# -*- coding: utf-8 -*-
# Copyright (C) 2026 Vertel Sverige AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
#
# Ported from the upstream ``mrp_workorder/models/mrp_bom.py``.
# The bill of materials needs the chatter (the Shop Floor posts
# feedback on it) and keeps the operation quality points in sync with the
# product.

from odoo import models


class MrpBom(models.Model):
    _name = 'mrp.bom'
    _inherit = ['mail.activity.mixin', 'mrp.bom']

    def write(self, vals):
        res = super().write(vals)
        if 'product_id' in vals or 'product_tmpl_id' in vals:
            self.operation_ids.quality_point_ids._change_product_ids_for_bom(self)
        return res
