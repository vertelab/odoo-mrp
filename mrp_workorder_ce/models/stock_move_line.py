# -*- coding: utf-8 -*-
# Copyright (C) 2026 Vertel Sverige AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
#
# Ported from the upstream ``mrp_workorder/models/stock_move_line.py``.
# Links move lines to their quality checks and keeps the lot in
# sync when the move line changes.

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    quality_check_ids = fields.One2many('quality.check', 'move_line_id', string='Check')

    def _without_quality_checks(self):
        self.ensure_one()
        return not self.quality_check_ids

    def write(self, vals):
        res = super().write(vals)
        if 'lot_id' in vals and self.sudo().quality_check_ids:
            self.sudo().quality_check_ids._update_lots()
        return res
