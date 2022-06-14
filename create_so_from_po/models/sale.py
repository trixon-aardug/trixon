# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_aa_tx_purchase_id = fields.Many2one('purchase.order', 'Purchase Order')
    x_aa_tx_vendor_id = fields.Many2one('res.partner', 'Vendor', related='x_aa_tx_purchase_id.partner_id')
    x_aa_tx_purchase_count = fields.Integer(string="purchase count",compute="x_aa_tx_purchase_order_count")

    def view_purchase_order(self):
        '''Open Purchase Order from Sale Order'''
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase Orders',
            'res_model':'purchase.order',
            'domain' : [('x_aa_tx_sale_id.id','=',self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }


    def x_aa_tx_purchase_order_count(self):
        ''' Order Count'''
        for rec in self:
            purchase_count = self.env['purchase.order'].search_count([('x_aa_tx_sale_id.id', '=', rec.id)])
            rec.x_aa_tx_purchase_count = purchase_count
