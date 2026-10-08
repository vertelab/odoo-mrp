# -*- coding: utf-8 -*-
# Copyright (C) 2026 Vertel AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
#
# Ported from the upstream ``mrp_workorder/models/stock_picking_type.py``.
# Opening the manufacturing operation type goes straight to the
# Shop Floor when there is only one.

from odoo import models


class PickingType(models.Model):
    _inherit = 'stock.picking.type'

    def action_mrp_overview(self):
        routing_count = self.env['stock.picking.type'].search_count([('code', '=', 'mrp_operation')])
        if routing_count == 1:
            return self.env['ir.actions.actions']._for_xml_id('mrp_workorder_ce.action_mrp_display')
        action = self.env['ir.actions.actions']._for_xml_id('mrp_workorder_ce.mrp_stock_picking_type_action')
        action['domain'] = [('code', '=', 'mrp_operation')]
        return action
