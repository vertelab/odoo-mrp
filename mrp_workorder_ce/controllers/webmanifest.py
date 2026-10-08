# -*- coding: utf-8 -*-
# Copyright (C) 2026 Vertel AB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
#
# Ported from the upstream ``mrp_workorder/controllers/webmanifest.py``.
# Gives the Shop Floor PWA its own icon.

from odoo import http
from odoo.http import request
from odoo.tools import file_open, image_process
from odoo.addons.web.controllers import webmanifest


class WebManifest(webmanifest.WebManifest):

    def _get_scoped_app_icons(self, app_id):
        if app_id == "mrp_shop_floor":
            return [{
            'src': '/mrp_workorder_ce/static/description/mrp_display_icon.svg',
            'sizes': 'any',
            'type': 'image/svg+xml'
            }]
        return super()._get_scoped_app_icons(app_id)

    @http.route()
    def scoped_app_icon_png(self, app_id):
        if app_id == "mrp_shop_floor":
            with file_open('mrp_workorder_ce/static/description/mrp_display_icon.png', 'rb') as file:
                image = image_process(file.read(), size=(180, 180), expand=True, colorize=(255, 255, 255), padding=16)
            return request.make_response(image, headers=[('Content-Type', 'image/png')])
        return super().scoped_app_icon_png(app_id)
