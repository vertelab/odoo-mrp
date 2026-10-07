# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2024- Vertel AB (<https://vertel.se>).
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
    'name': 'MRP: PLM CE',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Product Lifecycle Management (PLM)',
    'sequence': 155,
    'summary': """Manage engineering change orders on products, bills of material for Community Edition""",
    'author': 'Vertel Sverige AB',
    'maintainer': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-mrp/mrp_plm_ce',
    'repository': 'https://github.com/vertelab/odoo-mrp',
    'license': 'AGPL-3',
    'depends': ['mrp'],
    'description': """
Product Lifecycle Management (CE)
=================================

Community Edition port of `mrp_plm`.

* Versioning of Bill of Materials and Products
* Different approval flows possible depending on the type of change order

""",
    'data': [
        'security/mrp_plm.xml',
        'security/ir.model.access.csv',
        'data/mail_activity_type_data.xml',
        'data/mrp_data.xml',
        'views/mrp_bom_views.xml',
        'views/mrp_document_views.xml',
        'views/mrp_eco_views.xml',
        'views/product_views.xml',
        'views/mrp_production_views.xml',
        'report/mrp_report_bom_structure.xml',
    ],
    'demo': [
        'data/mrp_demo.xml',
    ],
    'application': True,
    'assets': {
        'web.assets_backend': [
            'mrp_plm_ce/static/src/**/*.js',
            'mrp_plm_ce/static/src/**/*.scss',
            'mrp_plm_ce/static/src/**/*.xml',
        ],
    }
}
