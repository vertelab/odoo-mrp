# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command
from odoo.addons.mrp_workorder_ce.tests.common import TestMrpWorkorderCommon
from odoo.tests import Form


class TestWorkOrderDependencies(TestMrpWorkorderCommon):
    """Operation dependencies on work orders (CE core feature).

    Ported from the upstream ``mrp_workorder/tests/test_dependencies.py``; the
    dependency logic itself lives in the CE core (``mrp``), so this test
    guards that the CE port does not disturb it.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.wkct1 = cls.env['mrp.workcenter'].create({
            'name': 'Workcenter#1',
        })
        cls.wkct2 = cls.env['mrp.workcenter'].create({
            'name': 'Workcenter#2',
        })
        cls.wkct3 = cls.env['mrp.workcenter'].create({
            'name': 'Workcenter#3',
        })
        cls.finished = cls.env['product.product'].create({
            'name': 'Finished Product',
            'is_storable': True,
        })
        cls.component1 = cls.env['product.product'].create({
            'name': 'Component#1',
            'is_storable': True,
        })
        cls.component2 = cls.env['product.product'].create({
            'name': 'Component#2',
            'is_storable': True,
        })
        cls.bom = cls.env['mrp.bom'].create({
            'product_id': cls.finished.id,
            'product_tmpl_id': cls.finished.product_tmpl_id.id,
            'product_qty': 1.0,
            'bom_line_ids': [
                Command.create({'product_id': cls.component1.id, 'product_qty': 1}),
                Command.create({'product_id': cls.component2.id, 'product_qty': 2}),
            ],
            'operation_ids': [
                Command.create({'name': 'Operation#A', 'workcenter_id': cls.wkct1.id}),
                Command.create({'name': 'Operation#B', 'workcenter_id': cls.wkct2.id}),
                Command.create({'name': 'Operation#C', 'workcenter_id': cls.wkct3.id}),
            ],
            'allow_operation_dependencies': True,
        })
        cls.stock_location = cls.env.ref('stock.stock_location_stock')
        cls.env['stock.quant']._update_available_quantity(cls.component1, cls.stock_location, 100)
        cls.env['stock.quant']._update_available_quantity(cls.component2, cls.stock_location, 100)

    def test_parallel_workorders(self):
        """Bom allowing operation dependencies without any dependency."""
        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.finished
        mo_form.product_qty = 2.0
        mo = mo_form.save()
        mo.action_confirm()

        self.assertEqual(mo.workorder_ids[0].state, 'ready', "All workorders should be ready.")
        self.assertEqual(mo.workorder_ids[1].state, 'ready', "All workorders should be ready.")
        self.assertEqual(mo.workorder_ids[2].state, 'ready', "All workorders should be ready.")

    def test_stepped_workorders(self):
        """Step-by-step workorders: bom operations are interdependent."""
        # Make 1st workorder depend on 3rd
        self.bom.operation_ids[0].blocked_by_operation_ids = [Command.link(self.bom.operation_ids[2].id)]

        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.finished
        mo_form.product_qty = 2.0
        mo = mo_form.save()
        mo.action_confirm()
        wo1, wo2, wo3 = mo.workorder_ids
        self.assertEqual(wo1.state, 'pending', "Operation-A should wait for the 3rd.")
        self.assertEqual(wo2.state, 'ready', "Operation-B should be ready.")
        self.assertEqual(wo3.state, 'ready', "Operation-C should be ready.")
        mo.button_plan()
        # Mark 1st initial WO as done
        wo2.button_start()
        wo2.qty_producing = 2
        wo2.button_finish()
        # Check 3rd WO (not dependent on 1st)
        self.assertEqual(wo1.state, 'pending', "Operation-A should STILL wait for the 3rd.")
        # Mark 2nd initial WO as done
        wo3.button_start()
        wo3.qty_producing = 2
        wo3.button_finish()
        # Check dependent WO
        self.assertEqual(wo1.state, 'ready', "Operation-A can start, its predecessors are done.")

    def test_allow_operation_dependency_with_deleted_workorder(self):
        """Removing a work order must not break the dependency chain."""
        self.bom.operation_ids[1].blocked_by_operation_ids = [Command.link(self.bom.operation_ids[0].id)]
        self.bom.operation_ids[2].blocked_by_operation_ids = [Command.link(self.bom.operation_ids[1].id)]

        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.finished
        mo_form.product_qty = 20
        mo = mo_form.save()

        self.assertEqual(mo.state, 'draft')

        wo_1, wo_2, wo_3 = mo.workorder_ids

        wo_2.unlink()
        mo.action_confirm()

        self.assertEqual(wo_1.state, 'ready')
        self.assertEqual(wo_3.state, 'ready')

        wo_1.button_start()
        wo_1.button_finish()

        wo_3.button_start()
        wo_3.button_finish()

        self.assertEqual(mo.state, 'to_close')
        mo.button_mark_done()
        self.assertEqual(mo.state, 'done')
        self.assertEqual(mo.workorder_ids.operation_id, self.bom.operation_ids[0] | self.bom.operation_ids[2])
