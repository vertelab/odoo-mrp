# Part of Odoo. See LICENSE file for full copyright and licensing details.
#
# Ported from the upstream ``mrp_workorder/tests/test_shopfloor.py``.
# Only the backend (non-tour) test is ported here: the tour tests
# need a browser and ``websocket-client``, which is not available on the
# build host. The tours belong to the frontend half of the port.
#
# ``TestShopFloor`` stays an ``HttpCase`` because
# ``quality_mrp_workorder_ce`` extends it and adds a tour test; that test is
# skipped when ``websocket-client`` is missing.
from odoo import Command
from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged('post_install', '-at_install')
class TestShopFloor(HttpCase):

    def setUp(self):
        super().setUp()
        # Set Administrator as the current user.
        self.uid = self.env.ref('base.user_admin').id
        # Enables Work Order setting, and disables other settings.
        group_workorder = self.env.ref('mrp.group_mrp_routings')
        self.env.user.write({'groups_id': [(4, group_workorder.id, 0)]})

        # Add some properties for commonly used in tests records.
        self.warehouse = self.env['stock.warehouse'].search([], limit=1)
        self.stock_location = self.warehouse.lot_stock_id

    def test_shop_floor_catalog_add_component_in_two_steps(self):
        """ Ensures when a component is added through the Shop Floor catalog,
        the Pick Component operation is correctly created/updated."""
        # Set the manufacture in 2 steps.
        self.warehouse.write({'manufacture_steps': 'pbm'})
        # Create a product with a BoM and two components.
        # Create some products.
        product_final = self.env['product.product'].create({
            'name': 'Pot',
            'is_storable': True,
        })
        product_comp1, product_comp2 = self.env['product.product'].create([{
            'name': 'C1 - Earthenware Clay',
            'is_storable': True,
        }, {
            'name': 'C2 - Stoneware Clay',
            'is_storable': True,
        }])
        bom = self.env['mrp.bom'].create({
            'product_id': product_final.id,
            'product_tmpl_id': product_final.product_tmpl_id.id,
            'product_uom_id': product_final.uom_id.id,
            'product_qty': 1.0,
            'consumption': 'flexible',
            'bom_line_ids': [
                Command.create({'product_id': product_comp1.id, 'product_qty': 1, 'manual_consumption': True}),
            ]
        })
        # Adds some quantity in stock.
        self.env['stock.quant']._update_available_quantity(product_comp1, self.stock_location, quantity=999)
        self.env['stock.quant']._update_available_quantity(product_comp2, self.stock_location, quantity=999)
        # Create a Manufacturing Order.
        mo = self.env['mrp.production'].create({
            'product_id': product_final.id,
            'product_qty': 1,
            'bom_id': bom.id,
        })
        mo.action_confirm()
        mo.action_assign()
        mo.button_plan()
        # Validate the MO's Pick Component.
        self.assertEqual(len(mo.picking_ids), 1)
        mo.picking_ids.button_validate()
        # Simulate "Add Component" from the Shop Floor.
        kwargs = {'from_shop_floor': True}
        mo._update_order_line_info(product_comp2.id, 1, 'move_raw_ids', **kwargs)
        self.assertEqual(len(mo.picking_ids), 2, "A second picking should have been created for the MO")
        self.assertEqual(mo.components_availability_state, 'available', "MO should still be ready nevertheless")
        second_picking = mo.picking_ids.filtered(lambda p: p.state == 'assigned')
        self.assertRecordValues(second_picking.move_ids, [
            {'product_id': product_comp2.id, 'product_uom_qty': 1, 'picked': False},
        ])
        self.assertRecordValues(mo.move_raw_ids, [
            {'product_id': product_comp1.id, 'product_uom_qty': 1, 'quantity': 1, 'picked': False},
            {'product_id': product_comp2.id, 'product_uom_qty': 1, 'quantity': 1, 'picked': False},
        ])
        # Simulate adding more quantity from the Shop Floor.
        mo._update_order_line_info(product_comp2.id, 2, 'move_raw_ids', **kwargs)
        self.assertEqual(len(mo.picking_ids), 2, "No other picking should have been created")
        self.assertEqual(mo.components_availability_state, 'available', "MO should still be ready")
        self.assertRecordValues(second_picking.move_ids, [
            {'product_id': product_comp2.id, 'product_uom_qty': 2, 'picked': False},
        ])
        self.assertRecordValues(mo.move_raw_ids, [
            {'product_id': product_comp1.id, 'product_uom_qty': 1, 'quantity': 1, 'picked': False},
            {'product_id': product_comp2.id, 'product_uom_qty': 2, 'quantity': 2, 'picked': False},
        ])
        # starts the MO and simulate adding more quantity from the Shop Floor.
        mo.action_start()
        self.assertEqual(mo.state, 'progress')
        mo._update_order_line_info(product_comp2.id, 3, 'move_raw_ids', **kwargs)
        self.assertEqual(len(mo.picking_ids), 2, "No other picking should have been created")
        self.assertEqual(mo.components_availability_state, 'available', "MO should still be ready")
        self.assertRecordValues(second_picking.move_ids, [
            {'product_id': product_comp2.id, 'product_uom_qty': 3, 'picked': False},
        ])
        self.assertRecordValues(mo.move_raw_ids, [
            {'product_id': product_comp1.id, 'product_uom_qty': 1, 'quantity': 1, 'picked': False},
            {'product_id': product_comp2.id, 'product_uom_qty': 3, 'quantity': 3, 'picked': False},
        ])
