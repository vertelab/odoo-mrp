# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2017- Vertel AB (<http://vertel.se>).
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

class mrp_repair(models.Model):
    _inherit = 'mrp.repair'

    @api.multi
    def action_confirm(self):
        res = super(mrp_repair, self).action_confirm()
        group = self.env['procurement.group'].create({})
        vals = {
            'name': 'Procurement %s' %self.product_id.name,
            'product_id': self.product_id.id,
            'product_qty': self.product_qty,
            'product_uom': self.product_uom.id,
            'location_id': self.location_id.id,
            'group_id': group.id,
        }
        group = self.env['procurement.order'].create(vals)
        return res
