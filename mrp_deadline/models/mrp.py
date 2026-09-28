from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    date_deadline = fields.Datetime(
        'Deadline', copy=False, store=True, readonly=False, compute='_compute_date_deadline', inverse='_inverse_date_deadline',
        help="Informative date allowing to define when the manufacturing order should be processed at the latest to fulfill delivery on time."
    )

    def _inverse_date_deadline(self):
        for production in self:
            if production.date_deadline:
                for sale in production.get_linked_sale_orders():
                    sale.commitment_date = production.date_deadline
                # Update ALL finished moves' deadlines to match production.date_deadline
                #finished_moves = production.move_finished_ids.filtered('date_deadline')
                #if finished_moves:
                #    finished_moves.sudo().write({'date_deadline': production.date_deadline})
                #    _logger.info("Inverse: Updated ALL %d finished moves to date_deadline %s for MO %s", len(finished_moves), production.date_deadline, production.name)
                #else:
                #    _logger.warning("No finished moves with date_deadline for MO %s", production.name)
