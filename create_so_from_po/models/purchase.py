# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    x_aa_tx_sale_id = fields.One2many('sale.order', 'x_aa_tx_purchase_id', 'Sale Order')
    x_aa_tx_sale_count = fields.Integer(string="sale count",compute="x_aa_tx_sale_order_count")





    def view_sale_order(self):
        '''Open Sale Order from Purchase Order'''
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model':'sale.order',
            'domain' : [('x_aa_tx_purchase_id','=',self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def x_aa_tx_sale_order_count(self):
        '''Sale Order Count'''
        for rec in self:
            sale_count = self.env['sale.order'].search_count([('x_aa_tx_purchase_id', '=', rec.id)])
            rec.x_aa_tx_sale_count = sale_count




class PurchaseOrderlines(models.Model):
    _inherit = 'purchase.order.line'

    x_aa_tx_sale_reference_no = fields.Char(string="Sale Reference")
