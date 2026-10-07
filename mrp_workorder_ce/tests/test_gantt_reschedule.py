# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta

from odoo import fields
from odoo.addons.mrp_workorder_ce.tests.common import TestMrpWorkorderCommon
from odoo.tests import Form


class TestGanttReschedule(TestMrpWorkorderCommon):
    """Work order rescheduling through the ``web_gantt_ce`` hooks."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.workcenter = cls.env['mrp.workcenter'].create({
            'name': 'Reschedule Workcenter',
        })
        cls.finished = cls.env['product.product'].create({
            'name': 'Reschedule Product',
            'is_storable': True,
        })
        cls.component = cls.env['product.product'].create({
            'name': 'Reschedule Component',
            'is_storable': True,
        })
        cls.bom = cls.env['mrp.bom'].create({
            'product_id': cls.finished.id,
            'product_tmpl_id': cls.finished.product_tmpl_id.id,
            'product_qty': 1.0,
            'bom_line_ids': [
                (0, 0, {'product_id': cls.component.id, 'product_qty': 1}),
            ],
            'operation_ids': [
                (0, 0, {'name': 'Reschedule Operation', 'workcenter_id': cls.workcenter.id}),
            ],
        })
        cls.stock_location = cls.env.ref('stock.stock_location_stock')
        cls.env['stock.quant']._update_available_quantity(cls.component, cls.stock_location, 100)

    def _make_workorder(self, qty=1.0):
        mo_form = Form(self.env['mrp.production'])
        mo_form.product_id = self.finished
        mo_form.product_qty = qty
        mo = mo_form.save()
        mo.action_confirm()
        mo.button_plan()
        return mo.workorder_ids[:1]

    def _reschedule(self, workorder, start, stop):
        return self.env['mrp.workorder'].web_gantt_reschedule(
            {
                'date_start': fields.Datetime.to_string(start),
                'date_finished': fields.Datetime.to_string(stop),
            },
            'maintainBuffer',
            workorder.ids,
            'blocked_by_workorder_ids',
            'needed_by_workorder_ids',
            'date_start',
            'date_finished',
        )

    def test_reschedule_snaps_to_workcenter_working_hours(self):
        """A move lands on the first available slot of the workcenter."""
        workorder = self._make_workorder()
        # A Sunday: the workcenter calendar has no working hours then.
        sunday = datetime(2026, 1, 4, 10, 0, 0)
        result = self._reschedule(workorder, sunday, sunday + timedelta(hours=1))
        self.assertEqual(result['type'], 'success')
        self.assertTrue(workorder.date_start)
        # The slot must fall on a working day (Monday or later).
        self.assertGreaterEqual(workorder.date_start.weekday(), 0)
        self.assertNotEqual(workorder.date_start.weekday(), 6, "Must not land on a Sunday.")
        # The duration is preserved.
        self.assertAlmostEqual(
            (workorder.date_finished - workorder.date_start).total_seconds(),
            workorder.duration_expected * 60,
            delta=60,
        )

    def test_progress_workorder_cannot_be_rescheduled(self):
        """A started work order may not be dragged."""
        workorder = self._make_workorder()
        workorder.button_start()
        self.assertEqual(workorder.state, 'progress')
        self.assertFalse(
            workorder._gantt_reschedule_is_candidate('date_start', 'date_finished'),
            "A work order in progress must not be reschedulable.",
        )
        before = (workorder.date_start, workorder.date_finished)
        monday = datetime(2026, 1, 5, 8, 0, 0)
        result = self._reschedule(workorder, monday, monday + timedelta(hours=1))
        self.assertEqual(result['type'], 'warning')
        self.assertEqual((workorder.date_start, workorder.date_finished), before)

    def test_done_workorder_cannot_be_rescheduled(self):
        """A finished work order may not be dragged."""
        workorder = self._make_workorder()
        workorder.button_start()
        workorder.qty_producing = 1
        workorder.button_finish()
        self.assertEqual(workorder.state, 'done')
        self.assertFalse(
            workorder._gantt_reschedule_is_candidate('date_start', 'date_finished'),
        )

    def test_ready_workorder_is_candidate(self):
        """A planned (ready) work order may be dragged."""
        workorder = self._make_workorder()
        self.assertIn(workorder.state, ('ready', 'waiting', 'pending'))
        self.assertTrue(
            workorder._gantt_reschedule_is_candidate('date_start', 'date_finished'),
        )

    def test_reschedule_relations_follow_dependencies(self):
        """The dependency chain is followed forward/backward.

        ``workorder`` is blocked by ``other``, so ``other`` is the
        predecessor. Moving forward follows the records that depend on
        this one (``needed_by_workorder_ids``); moving backward follows
        the records this one depends on (``blocked_by_workorder_ids``).
        """
        workorder = self._make_workorder()
        other = self._make_workorder()
        workorder.blocked_by_workorder_ids = [(6, 0, other.ids)]

        forward = workorder._gantt_reschedule_relations(
            'blocked_by_workorder_ids', 'needed_by_workorder_ids',
            search_forward=True,
        )
        self.assertFalse(forward, "Nothing depends on the work order yet.")

        backward = workorder._gantt_reschedule_relations(
            'blocked_by_workorder_ids', 'needed_by_workorder_ids',
            search_forward=False,
        )
        self.assertEqual(backward, other)

        # The predecessor follows its successor when the move goes forward.
        forward_from_other = other._gantt_reschedule_relations(
            'blocked_by_workorder_ids', 'needed_by_workorder_ids',
            search_forward=True,
        )
        self.assertEqual(forward_from_other, workorder)
