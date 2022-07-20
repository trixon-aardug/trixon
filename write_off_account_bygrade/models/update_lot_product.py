# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields


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
                for aa in variants:
                    if aa.attribute_id.with_context(lang='en_US').name == 'Grade':
                        dynamic_domain += ('product_template_variant_value_ids', 'not in', [aa.id]),
                    else:
                        dynamic_domain += ('product_template_variant_value_ids', 'in', [aa.id]),
                return dynamic_domain

    x_aa_tx_product_id = fields.Many2one('product.product', 'Product', required=True, domain=_domain_show_product)


    def update_grade(self):
        find_lot = self.env['stock.production.lot'].browse(self._context.get('active_id'))
        result = find_lot.action_scrap_lot()
        grade_value = ''
        for record in self:
            for attrs in record.x_aa_tx_product_id.product_template_variant_value_ids:
                if attrs.attribute_id.with_context(lang='en_US').name == 'Grade':
                    grade_value = attrs.product_attribute_value_id.with_context(lang='nl_NL').name
            create_lot = self.env['stock.production.lot'].create({
            'product_id': record.x_aa_tx_product_id.id,
            'company_id': self.env.company.id,
            'name': find_lot.name,
            'x_aa_tx_booked': find_lot.x_aa_tx_booked,
            'x_aa_tx_name': find_lot.x_aa_tx_name,
            'x_aa_tx_extern_id': find_lot.x_aa_tx_extern_id,
            'x_aa_tx_intern_id': find_lot.x_aa_tx_intern_id,
            'x_aa_tx_imei': find_lot.x_aa_tx_imei,
            'x_aa_tx_brand_id': find_lot.x_aa_tx_brand_id.id,
            'x_aa_tx_model_id': find_lot.x_aa_tx_model_id.id,
            'x_aa_tx_storage': find_lot.x_aa_tx_storage,
            'x_aa_tx_graphics_card': find_lot.x_aa_tx_graphics_card,
            'x_aa_tx_memory': find_lot.x_aa_tx_memory,
            'x_aa_tx_keyboard': find_lot.x_aa_tx_keyboard,
            'x_aa_tx_colour': find_lot.x_aa_tx_colour,
            'x_aa_tx_dual_sim': find_lot.x_aa_tx_dual_sim,
            'x_aa_tx_ssd': find_lot.x_aa_tx_ssd,
            'x_aa_tx_cpu': find_lot.x_aa_tx_cpu,
            'x_aa_tx_other_remarks': find_lot.x_aa_tx_other_remarks,
            'x_aa_tx_tag_ids' : find_lot.x_aa_tx_tag_ids,
            'x_aa_tx_grade' : grade_value,
            })
            self.env['stock.quant'].sudo().create({
            'product_id': record.x_aa_tx_product_id.id,
            'location_id': self.env.user._get_default_warehouse_id().lot_stock_id.id,
            'lot_id': create_lot.id,
            'inventory_quantity': 1.0,
            }).action_apply_inventory()
        return create_lot

