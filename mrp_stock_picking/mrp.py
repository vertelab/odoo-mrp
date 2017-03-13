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

import logging
_logger = logging.getLogger(__name__)

class MRPProduction(models.Model):
    _inherit = 'mrp.production'
    
    picking_ids = fields.Many2many(comodel_name='stock.picking', string='Stock Pickings')
    
    @api.model
    def action_produce(self, production_id, production_qty, production_mode, wiz=False):
        if wiz:
            production = self.browse(production_id)
            picking = None
            for p in production.picking_ids:
                if p.state == 'draft':
                    picking = p
            if not picking:
                picking = self.env['stock.picking'].create({
                    'picking_type_id': self.env.ref('mrp_stock_picking.production_picking_type').id,
                })
                production.picking_ids |= picking
            picking.move_lines |= self.env['stock.move'].create({
                'name': wiz.product_id.partner_ref,
                'product_id': wiz.product_id.id,
                'product_uom': wiz.product_id.uom_id.id,
                'product_uos': wiz.product_id.uos_id and wiz.product_id.uos_id.id,
                'product_uom_qty': wiz.product_qty,
                'location_id': production.location_dest_id.id,
                'location_dest_id': wiz.product_id.property_stock_procurement.id,
                'state': 'draft',
            })
        res = super(MRPProduction, self).action_produce(production_id, production_qty, production_mode, wiz=False)
        return res
    
    @api.multi
    def action_production_end(self):
        _logger.warn('\n\n\nhej hej!\n\n\n')
        res = super(MRPProduction, self).action_production_end()
        for record in self:
            for picking in record.picking_ids:
                _logger.warn(picking)
                if picking.state in ('draft', 'confirmed'):
                    picking.action_assign()
        return res

