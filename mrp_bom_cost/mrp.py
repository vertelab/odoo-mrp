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

    @api.one
    def _uom_cost(self):
        self.uom_cost = self.product_uom._compute_price(self.product_id.uom_id.id, self.product_id.standard_price, to_uom_id=self.product_uom.id)
    uom_cost = fields.Float(string='Unit Cost',compute="_uom_cost")
    @api.one
    def _material_cost(self):
        self.material_cost = self.product_qty * self.uom_cost
    material_cost = fields.Float(string='Material Cost', compute='_material_cost')

class mrp_bom(models.Model):
    _inherit = 'mrp.bom'

    @api.one
    def _material_cost(self):
        self.material_cost = sum([l.material_cost for l in self.bom_line_ids])
    material_cost = fields.Float(string='Material Cost', compute="_material_cost")


class mrp_bom_line(models.Model):
    _inherit = 'mrp.bom.line'

    @api.one
    def _uom_cost(self):
        self.uom_cost = self.product_uom._compute_price(self.product_id.uom_id.id, self.product_id.standard_price, to_uom_id=self.product_uom.id)
    uom_cost = fields.Float(string='Unit Cost',compute="_uom_cost")
    @api.one
    def _material_cost(self):
        self.material_cost = self.product_qty * self.uom_cost
    material_cost = fields.Float(string='Material Cost', compute='_material_cost')

