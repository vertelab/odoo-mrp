from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    date_deadline = fields.Datetime(
        'Deadline', copy=False, store=True, readonly=False,
        compute='_compute_date_deadline', inverse='_inverse_date_deadline',
        help="Informative date allowing to define when the manufacturing "
             "order should be processed at the latest to fulfill delivery "
             "on time."
    )

    def _inverse_date_deadline(self):
        for production in self:
            if not production.date_deadline:
                continue
            # ``get_linked_sale_orders`` is provided by ``sale_mrp``. That
            # module is optional, so only propagate the deadline when the
            # link between a manufacturing order and its sale orders is
            # actually available.
            if not hasattr(production, 'get_linked_sale_orders'):
                continue
            for sale in production.get_linked_sale_orders():
                sale.commitment_date = production.date_deadline
