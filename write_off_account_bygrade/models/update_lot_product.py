# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import _, api, models, fields


class SalePurchaseOrder(models.TransientModel):
    _name = 'update.lot.product.wizard'
    _description = 'Update Lot Product'

    def _domain_show_product(self):
        ''' This method used to show a specific products only'''
        if self.env.context.get('active_model') == 'stock.production.lot' and self.env.context.get('active_id'):
            find_lot = self.env['stock.production.lot'].browse(self.env.context.get('active_id'))
            variants = find_lot.product_id.product_template_variant_value_ids
            if variants:
                dynamic_domain = []
                for aa in variants[0:-1]:
                    dynamic_domain += ('product_template_variant_value_ids', 'in', [aa.id]),
                for aa in variants[-1]:
                    dynamic_domain += ('product_template_variant_value_ids', 'not in', [aa.id]),
                return dynamic_domain

    x_aa_tx_product_id = fields.Many2one('product.product', 'Product', required=True, domain=_domain_show_product)


    def update_grade(self):
        find_lot = self.env['stock.production.lot'].browse(self._context.get('active_id'))
        result = find_lot.action_scrap_lot()
        for record in self:
            create_lot = self.env['stock.production.lot'].create({
            'product_id': record.x_aa_tx_product_id.id,
            'company_id': self.env.company.id,
            'name': find_lot.name,
            })
            self.env['stock.quant'].sudo().create({
            'product_id': record.x_aa_tx_product_id.id,
            'location_id': self.env.user._get_default_warehouse_id().lot_stock_id.id,
            'lot_id': create_lot.id,
            'inventory_quantity': 1.0,
            }).action_apply_inventory()
        return create_lot

