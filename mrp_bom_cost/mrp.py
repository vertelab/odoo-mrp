# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2016 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class mrp_production_product_line(models.Model):
    _inherit = 'mrp.production.product.line'

    line_uom_cost = fields.Float(string='Unit Cost', related='product_id.standard_price')
    line_material_cost = fields.Float(string='Material Cost', compute='_line_material_cal')

    @api.one
    def _line_material_cal(self):
        self.line_material_cost = self.product_id.standard_price * self.product_qty

class mrp_bom(models.Model):
    _inherit = 'mrp.bom'

    @api.one
    def _material_cost(self):
        self.product_cost = sum([l.material_cost for l in self.bom_line_ids])
    material_cost = fields.Float(string='Material Cost', compute="_material_cost")
   

class mrp_bom_line(models.Model):
    _inherit = 'mrp.bom.line'

    @api.one
    def _uom_cost(self):
        self.line_uom_cost = round(self.product_id.standard_price * self.product_uom.factor,self.product_uom.rounding) * 750.0
    uom_cost = fields.Float(string='Unit Cost',compute="_line_uom_cost")
    @api.one
    def _material_cost(self):
        self.line_material_cost = self.product_id.standard_price * self.line_uom_cost
    material_cost = fields.Float(string='Material Cost', compute='_material_cost')

