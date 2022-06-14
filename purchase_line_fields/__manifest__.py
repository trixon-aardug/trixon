# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Purchase Line Fields',
    'version': '15.0.0.1',
    'summary': """
    Customization for Purchase Line Fields.
    """,
    'description': """
        * Add Custom Fields like SKU, Serial, Grade, Battery Condition,
        Note and Sold on PO Line.
    """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'category': 'Purchase',
    'depends': ['purchase', 'stock', 'sale'],
    'data': [
             'security/ir.model.access.csv',
             'views/purchase_views.xml',
             'views/stock_move_view.xml',
             'views/sale_view.xml',
             'views/stock_production_lot_views.xml',
             'views/mobile_brand_page_view.xml',
             'views/mobile_model_page_view.xml',
             'views/mobile_storage_page_view.xml',
             'views/mobile_brand_view.xml',
             ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
