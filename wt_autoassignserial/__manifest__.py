# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Sale/Delivery Auto Assign Serial number",
    "author": "Warlock Technologies Pvt Ltd.",
    "website": "http://warlocktechnologies.com",
    "description": """Sale/Delivery Auto Assign Serial number""",
    "summary": """Put serial number in sale order line get product using that serial number and use that serial number in delivery order""",
    "version": "15.0.1.0",
    "price": 30.00,
    "currency": "USD",
    "support": "info@warlocktechnologies.com",
    "license": "OPL-1",
    "category": "Users",
    "depends": ["base", "sale_management", "stock"],
    "data": [
        "views/sale_order_view.xml",
    ],
    "images": ["images/screen_image.png"],
    "demo": [],
    "installable": True,
}
