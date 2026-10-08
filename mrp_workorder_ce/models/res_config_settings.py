# -*- coding: utf-8 -*-
# Copyright (C) 2026 Vertel Sverige AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
#
# Ported from the upstream ``mrp_workorder/models/res_config_settings.py``.
# Shop Floor and timer groups in the manufacturing settings, and
# the byproduct check type activation.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_mrp_wo_tablet_timer = fields.Boolean("Timer", implied_group="mrp_workorder_ce.group_mrp_wo_tablet_timer")
    group_mrp_wo_shop_floor = fields.Boolean("Shop Floor", implied_group="mrp_workorder_ce.group_mrp_wo_shop_floor")

    def set_values(self):
        super().set_values()
        if not self.env.user.has_group('mrp.group_mrp_manager'):
            return
        register_byproducts = self.env.ref('mrp_workorder_ce.test_type_register_byproducts').sudo()
        if register_byproducts.active != self.group_mrp_byproducts:
            register_byproducts.active = self.group_mrp_byproducts
