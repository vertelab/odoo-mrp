{
    "name": "MRP Deadline Editor",
    "version": "18.0.1.0.0",
    "category": "Manufacturing",
    "summary": "Allow manual editing of Manufacturing Order deadline",
    "description": """
Adds custom logic to make the Manufacturing Order deadline editable.
""",
    "author": "Your Name",
    "website": "https://vertel.se/apps/odoo-mrp/mrp_deadline",
    "license": "AGPL-3",
    "depends": ["mrp","sale","stock"],
    "data": [
        "views/mrp_production_views.xml",
    ],
    "installable": True,
    "application": False,
}
