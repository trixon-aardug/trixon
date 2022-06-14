# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Aardug. (Website: www.aardug.nl).                                  #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': 'Create SO From PO',
    'version': '15.0.0.1',
    'summary': """
    Create Sale order from purchase order.
    """,
    'description': """ """,
    'author': 'Aardug, Arjan Rosman',
    'website': 'http://www.aardug.nl/',
    'category': 'Sale',
    'depends': ['purchase', 'sale'],
    'data': [
             'security/ir.model.access.csv',
             'views/purchase_wizard_views.xml',
             'views/purchase_views.xml',
             'views/sale_view.xml',
             ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
