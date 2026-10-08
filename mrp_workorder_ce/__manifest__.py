# -*- coding: utf-8 -*-
##############################################################################
#
#    Vertel AB, Open Source Management Solution, third party addon
#    Copyright (C) 2026- Vertel AB (<https://vertel.se>).
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
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'MRP: Work Orders CE',
    'version': '18.0.1.1.0',
    'category': 'Manufacturing/Manufacturing',
    'sequence': 51,
    'summary': """Work order planning in Gantt and the Shop Floor (MES) backend.""",
    'author': 'Vertel Sverige AB',
    'maintainer': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-mrp/mrp_workorder_ce',
    'repository': 'https://github.com/vertelab/odoo-mrp',
    'license': 'AGPL-3',
    # Only ``quality_ce`` (the base quality app), exactly like the upstream module's
    # ``mrp_workorder`` depends on ``quality``.
# The bridge in
    # ``models/quality.py`` defines ``quality.check.production_id`` itself,
    # so ``quality_mrp_ce`` is not needed here. Depending on
    # ``quality_mrp_ce`` directly would pull it in *without*
    # ``quality_mrp_workorder_ce`` on a bare ``-i mrp_workorder_ce`` install,
    # and that pair-less state leaks operation-bound quality points into
    # production-level checks (breaking ``test_backorder_1``). The
    # ``quality_mrp_workorder_ce`` module (odoo-quality) pulls the
    # ``quality_control_ce`` / ``quality_mrp_ce`` chain when it is installed.
    'depends': ['mrp', 'web_gantt_ce', 'web_tour', 'barcodes', 'hr_hourly_cost',
                'quality_ce'],
    'description': """
MRP: Work Orders CE
===================

Community Edition port of ``mrp_workorder`` (MRP II).

Planning (step 1):

* **Planning by Production** — Gantt grouped by manufacturing order.
* **Planning by Workcenter** — Gantt grouped by workcenter, with the
  workcenter unavailability shading and the workcenter progress bar.

Both views are also available with operation dependencies enabled
(``blocked_by_workorder_ids`` / ``needed_by_workorder_ids``), and dragging
a pill reschedules the work order onto the first available slot of its
workcenter.

Shop Floor / MES (step 2):

* The ``action_mrp_display`` client action and the ``Shop Floor`` menu.
* The MES backend methods on ``mrp.workorder`` (``button_start``,
  ``button_finish``, ``record_production``, ``do_finish``,
  ``verify_quality_checks``, ``_create_checks``, ``action_open_mes`` …).
* The quality bridge (``quality.point.operation_id`` and the checks the
  Shop Floor creates for it).
* The employees allowed on a workcenter and the employee hourly cost.
* The additional work order and propose change wizards.

The OWL tablet application (``static/src/mrp_display/``) is step 2's
frontend half and is delivered separately.
""",
    'data': [
        'security/ir.model.access.csv',
        'security/mrp_workorder_security.xml',
        'data/mrp_workorder_data.xml',
        'views/hr_employee_views.xml',
        'views/quality_views.xml',
        'views/mrp_bom_views.xml',
        'views/mrp_workorder_views.xml',
        'views/mrp_operation_views.xml',
        'views/mrp_production_views.xml',
        'views/mrp_workcenter_views.xml',
        'views/stock_picking_type_views.xml',
        'views/res_config_settings_view.xml',
        'views/mrp_workorder_views_menus.xml',
        'wizard/additional_workorder_views.xml',
        'wizard/propose_change_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mrp_workorder_ce/static/src/mrp_workorder_gantt_view.scss',
        ],
        'web.assets_backend_lazy': [
            'mrp_workorder_ce/static/src/mrp_workorder_gantt_view.js',
            'mrp_workorder_ce/static/src/mrp_workorder_gantt_renderer.js',
            'mrp_workorder_ce/static/src/mrp_workorder_gantt_row_progress_bar.js',
            'mrp_workorder_ce/static/src/mrp_workorder_gantt_row_progress_bar.xml',
        ],
        'web.assets_unit_tests': [
            'mrp_workorder_ce/static/tests/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
