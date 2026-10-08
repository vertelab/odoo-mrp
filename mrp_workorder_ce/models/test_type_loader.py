# -*- coding: utf-8 -*-
# Copyright (C) 2026 Vertel Sverige AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.tools.convert import convert_file


class MrpWorkorderTestTypeLoader(models.AbstractModel):
    """Load the Shop Floor check types when the quality model exists.

    The four ``quality.point.test_type`` records belong to the upstream module's
    ``mrp_workorder`` (the Shop Floor flow), but the model itself comes from
    ``quality_ce``. Listing them directly in the manifest would break the
    install of step 1 (planning), which must work without the quality fork.
    They are loaded from a ``<function>`` (see ``data/mrp_workorder_data.xml``)
    instead, and only when ``quality.point.test_type`` is registered.

    A ``<function>`` is re-run on every install/update of this module, so the
    records are also created when ``quality_ce`` is installed *after* this
    module (the step-1-then-quality-fork ordering).
    """

    _name = 'mrp.workorder.test.type.loader'
    _description = 'Shop Floor check type loader'

    @api.model
    def load_shopfloor_test_types(self):
        if 'quality.point.test_type' not in self.env:
            return
        convert_file(
            self.env, 'mrp_workorder_ce',
            'data/mrp_workorder_test_type.xml', {}, mode='init',
            noupdate=True,
        )
