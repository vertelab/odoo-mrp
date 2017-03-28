# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2016- Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, _
import math

import logging
_logger = logging.getLogger(__name__)


class mrp_mo_pack_labels(models.TransientModel):
    _name = 'mrp.mo_pack_labels.wizard'

    @api.model
    def _nbr_labels(self):
        return math.floor(self.get_moves()[0].product_uom_qty / self.get_moves()[0].packaging_qty)
    nbr_labels = fields.Integer(default=_nbr_labels)

    def get_moves(self):
        stock_move = self.env['stock.move'].browse([])
        for mrp in self.env['mrp.production'].browse(self._context.get('active_ids', [])):
            stock_move |= mrp.move_created_ids2 
        return stock_move

    @api.multi
    def print_label(self):
        self.ensure_one()
        stock_move = self.env['stock.move'].browse([])        
        for move in self.get_moves():
            for _ in range(self.nbr_labels if self.nbr_labels > 0 else math.floor(move.product_uom_qty / move.packaging_qty)):
                stock_move |= move
        return self.env['report'].get_action(stock_move, self.env.ref('mrp_mo_labels.mo_pack_label').report_name)

class stock_move(models.Model):
    _inherit = 'stock.move'
    
    @api.one
    def _packaging_qty(self):  # The least package are production (?)
        self.packaging_qty = self.product_id.packaging_ids.sorted(lambda p: p.qty).mapped('qty')[0] if len(self.product_id.packaging_ids.mapped('qty')) > 0 else 30
    packaging_qty = fields.Integer(compute='_packaging_qty')
    product_name = fields.Char(related='product_id.name')
    product_default_code = fields.Char(related='product_id.default_code')
    product_ean13 = fields.Char(related='product_id.ean13')
    product_uom_name = fields.Char(related='product_id.uom_id.name')
    restrict_lot_id_name = fields.Char(related='restrict_lot_id.name')
    