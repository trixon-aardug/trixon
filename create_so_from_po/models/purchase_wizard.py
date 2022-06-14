# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models


class SalePurchaseOrder(models.TransientModel):
    _name = 'sale.order.wizard'
    _description = 'create so from po'


    def _default_line_ids(self):
        pr_lines = []
        po_line_ids = self.env['purchase.order.line'].search([('order_id', '=', self._context.get('active_id'))]).filtered(lambda line: not line.x_aa_tx_is_sold)
        for po_line_id in po_line_ids:
            pr_lines.append((0, 0, {
                'x_aa_tx_product_id': po_line_id.product_id.id,
                'x_aa_tx_product_qty': po_line_id.product_qty,
                'x_aa_tx_serial': po_line_id.x_aa_tx_serial,
            }))
        return pr_lines

    x_aa_tx_purchase_id = fields.Many2one('purchase.order', 'Purchase Order')
    x_aa_tx_partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    x_aa_tx_order_line = fields.One2many('purchase.order.line.wizard', 'x_aa_tx_purchase_line_id', default=_default_line_ids)


    def update_pol(self):
        for record in self:
            create_so_order = self.env['sale.order'].create({
                'partner_id': record.x_aa_tx_partner_id.id,
                'x_aa_tx_purchase_id': record.x_aa_tx_purchase_id.id,
                })
            for line in record.x_aa_tx_order_line:
                find_lot_id = self.env['stock.production.lot'].search([('name', '=', line.x_aa_tx_serial)])
                self.env['sale.order.line'].create({
                    'product_id': line.x_aa_tx_product_id.id,
                    'product_uom_qty': line.x_aa_tx_product_qty,
                    'lot_ids': [(6, 0, find_lot_id.ids)],
                    'order_id': create_so_order.id,
                })
        ((record.x_aa_tx_purchase_id).order_line).filtered(lambda line: not line.x_aa_tx_is_sold).write({
            'x_aa_tx_sale_reference_no' : create_so_order.name,
            'x_aa_tx_is_sold' : True,
        })
        return create_so_order


class PurchaseOrderLineWizard(models.TransientModel):
    _name = 'purchase.order.line.wizard'
    _description = 'Purchase Order Line Wizard'

    x_aa_tx_purchase_line_id = fields.Many2one('sale.order.wizard')
    x_aa_tx_product_id = fields.Many2one('product.product', 'Product')
    x_aa_tx_product_qty = fields.Float(string='Quantity', digits='Product Unit of Measure')
    x_aa_tx_serial = fields.Char("Serial")
