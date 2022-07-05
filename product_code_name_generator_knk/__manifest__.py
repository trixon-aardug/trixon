# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).
{
    "name": 'Product Code/Name Generator',
    'version': '15.0.1.0',
    'summary': 'Product Code/Name Generator module allows user to add various code as well as name in Product Internal Reference and product name respectively.| Generate | Product | Default | code| Attribute | value | Category |',
    'category': 'Sales/Sales',
    'website': 'https://www.kanakinfosystems.com',
    'author': 'Kanak Infosystems LLP.',
    'description': """
        => Generate Product Internal Reference.
        => Set Code in Category
        => Add Attributes in Category
        => Add to display code or name in attribute
        => Add Code to attribute value.
        => Select Products and generate Product Internal Reference as well as name.
    """,
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_category_view.xml',
        'views/product_product_views.xml',
    ],
    'images': ['static/description/banner.gif'],
    "installable": True,
    'license': 'OPL-1',
    'price': 16.87,
    'currency': 'EUR',
}
