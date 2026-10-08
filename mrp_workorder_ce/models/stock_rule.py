# -*- coding: utf-8 -*-
# Copyright (C) 2026 Vertel AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
#
# Ported from the upstream ``mrp_workorder/models/stock_rule.py``.
# A reordering rule must not update a manufacturing order whose
# quality checks have already been performed; it creates a new MO instead.

from odoo import models
from odoo.osv import expression


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _make_mo_get_domain(self, procurement, bom):
        domain = super()._make_mo_get_domain(procurement, bom)
        return tuple(
            expression.AND([
                list(domain),
                expression.OR([
                    [('check_ids', '=', False)],
                    [('check_ids', 'not any', [('quality_state', '!=', 'none')])]
                ]),
                expression.OR([
                    [('workorder_ids', '=', False)],
                    [('workorder_ids', 'not any',
                        [
                            ('check_ids', '!=', False),
                            ('check_ids', 'any', [('quality_state', '!=', 'none')])
                        ]
                    )]
                ])
            ])
        )
