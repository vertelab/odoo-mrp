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
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'sequence': 51,
    'summary': """Work order planning in Gantt (Planning by Production / by Workcenter).""",
    'author': 'Vertel Sverige AB',
    'maintainer': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-mrp/mrp_workorder_ce',
    'repository': 'https://github.com/vertelab/odoo-mrp',
    'license': 'AGPL-3',
    'depends': ['mrp', 'web_gantt_ce', 'web_tour', 'barcodes', 'hr_hourly_cost'],
    'description': """
MRP: Work Orders CE
===================

Community Edition port of the planning half of the upstream
``mrp_workorder`` (MRP II).

Adds the two work order planning views that the upstream module ships on top of the
Community Edition core:

* **Planning by Production** — Gantt grouped by manufacturing order.
* **Planning by Workcenter** — Gantt grouped by workcenter, with the
  workcenter unavailability shading and the workcenter progress bar.

Both views are also available with operation dependencies enabled
(``blocked_by_workorder_ids`` / ``needed_by_workorder_ids``), and dragging
a pill reschedules the work order onto the first available slot of its
workcenter.

The Shop Floor / MES tablet application is **not** part of this module.
It is step 2 of the change and is blocked by the quality fork; see
``openspec/changes/mrp-workorder-ce`` in the planning repository.
""",
    'data': [
        'security/mrp_workorder_security.xml',
        'data/mrp_workorder_data.xml',
        'views/mrp_workorder_views.xml',
        'views/mrp_production_views.xml',
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
