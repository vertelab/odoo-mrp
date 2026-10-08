# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2024- Vertel Sverige AB (<https://vertel.se>).
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
    'name': 'MRP: Master Production Schedule CE',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'sequence': 50,
    'summary': 'Master Production Schedule for Community Edition',
    'author': 'Vertel Sverige AB',
    'maintainer': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-mrp/mrp_mps_ce',
    'repository': 'https://github.com/vertelab/odoo-mrp',
    'license': 'AGPL-3',
    'depends': ['base_import', 'mrp', 'purchase_stock'],
    'description': """
Master Production Schedule (CE)
================================

Community Edition port of `mrp_mps`.

Sometimes you need to create the purchase orders for the components of
manufacturing orders that will only be created later.  Or for production orders
where you will only have the sales orders later.  The solution is to predict
your sale forecasts and based on that you will already create some production
orders or purchase orders.

You need to choose the products you want to add to the report.  You can choose
the period for the report: day, week, month, ...  It is also possible to define
safety stock, min/max to supply and to manually override the amount you will
procure.
""",
    'data': [
        'data/ir_cron_data.xml',
        'security/ir.model.access.csv',
        'security/mrp_mps_security.xml',
        'views/mrp_mps_views.xml',
        'views/mrp_mps_menu_views.xml',
        'views/mrp_bom_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/mrp_mps_forecast_details_views.xml'
    ],
    'demo': [
        'data/mps_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mrp_mps_ce/static/src/**/*',
        ],
    }
}
