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
    _inherit = 'mrp.production.workcenter.line'

    color = fields.Integer('Color')
    #~ date_planned_end = fields.Datetime(compute='_get_date_end_store', string='End Date', store=True)
    
    #~ @api.one
    #~ @api.depends('date_planned', 'hour', 'workcenter_id', 'workcenter_id.calendar_id')
    #~ def _get_date_end_store(self):
        #~ if self.date_planned and self.workcenter_id.calendar_id:
            #~ date_and_hours_by_cal = [(self.date_planned, self.hour, self.workcenter_id.calendar_id.id)]
            #~ intervals = self.env['resource.calendar'].interval_get_multi(date_and_hours_by_cal)
            #~ i = intervals.get((self.date_planned, self.hour, self.workcenter_id.calendar_id.id))
            #~ if i:
                #~ self.date_planned_end = i[-1][1].strftime('%Y-%m-%d %H:%M:%S')
            #~ else:
                #~ self.date_planned_end = op.date_planned
    
    #~ @api.one
    #~ def _check_workcenter_collisions(self):
        #~ if self.date_planned and self.date_planned_end:
            #~ previous = self.env['mrp.production.workcenter.line'].search([
                #~ ('workcenter_id', '=', self.workcenter_id.id),
                #~ ('date_planned', '<=', self.date_planned),
                #~ ('id', '!=', self.id)], limit = 1, order = 'date_planned DESC')
            #~ if previous and previous.date_planned_end > self.date_planned:
                #~ _logger.warn(previous)
                #~ self.date_planned = previous.date_planned_end
            #~ _logger.warn(self.date_planned)
            #~ _logger.warn(self.date_planned_end)
            #~ overlapping = self.env['mrp.production.workcenter.line'].search([
                #~ ('workcenter_id', '=', self.workcenter_id.id),
                #~ ('date_planned', '>=', self.date_planned),
                #~ ('date_planned', '>', self.date_planned_end)], order = 'date_planned')
            #~ _logger.warn(overlapping)
            #~ for line in overlapping:
                #~ line.date_planned = self.date_planned_end

