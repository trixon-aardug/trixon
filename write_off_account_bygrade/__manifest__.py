# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Write Off Account By Grade',
    'version': '15.0.0.1',
    'summary': """
    Write Off Product Account By its Grade.
    """,
    'description': """ This Module allows to change Products Grade From a Serial Number """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'category': 'Sale',
    'depends': ['product', 'stock_lot_scrap'],
    'data': [
            'security/ir.model.access.csv',
             'views/stock_production_lot_views.xml',
             ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
