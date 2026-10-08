# -*- coding: utf-8 -*-
# Copyright (C) 2026 Vertel Sverige AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
#
# Ported from the upstream ``mrp_workorder/wizard/change_production_qty.py``.
# Blocks updating the quantity to do of a manufacturing order whose
# quality checks have already been performed.

from odoo import models, _
from odoo.exceptions import ValidationError


class ChangeProductionQty(models.TransientModel):
    _inherit = "change.production.qty"

    def change_prod_qty(self):
        super(ChangeProductionQty, self).change_prod_qty()
        # if there are quality checks, we should create new checks/update the quantities, etc.
        # if we want to make this feature work, a task should be done to deal with all the possible cases:
        # types of quality check, quantity processed, etc. In the meantime, we block this feature.
        for wizard in self:
            done_checks = self.env['quality.check'].search([
                '&', ('control_date', '!=', False),
                '|', ('production_id', '=', wizard.mo_id.id), ('workorder_id', 'in', wizard.mo_id.workorder_ids.ids),
            ])
            if done_checks:
                raise ValidationError(_("You cannot update the quantity to do of an ongoing "
                                        "manufacturing order for which quality checks have been performed."))
