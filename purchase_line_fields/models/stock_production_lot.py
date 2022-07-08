# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields, api


class ProductTemplateGrade(models.Model):
    _inherit = 'product.product'

    x_aa_tx_grade = fields.Selection([
        ('aa','AA'),
        ('a','A'),
        ('b','B'),
        ('c','C'),
        ('d','D')], string="Grade")


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    x_aa_tx_grade = fields.Char('Grade')
    x_aa_tx_battery_condition = fields.Char("Battery Condition")
    x_aa_tx_note = fields.Char("Note")
    x_aa_tx_booked = fields.Selection([('1', 'True'), 
        ('0', 'Not True')], string="Booked")
    x_aa_tx_name = fields.Selection([('wubbo', 'Wubbo'), 
        ('marwin', 'Marwin'), 
        ('yusuf', 'Yusuf'),
        ('jeffery', 'Jeffery'),
        ('stan', 'Stan'), 
        ('christiaan', 'Christiaan'),
        ('richard', 'Richard')], string='Name')
    x_aa_tx_extern_id = fields.Char('Extern ID')
    x_aa_tx_intern_id = fields.Integer('Intern ID')
    x_aa_tx_imei = fields.Integer('IMEI')
    x_aa_tx_brand_id = fields.Many2one('mobile.brand', 'Brand')
    x_aa_tx_model_id = fields.Many2one('mobile.model', 'Model', 
        domain="[('x_aa_tx_brand_id', '=', x_aa_tx_brand_id)]")
    x_aa_tx_storage = fields.Char('Storage')
    x_aa_tx_graphics_card = fields.Char('Graphics Card')
    x_aa_tx_memory = fields.Char('Memory')
    x_aa_tx_dual_sim = fields.Char('Dual Sim')
    x_aa_tx_ssd = fields.Char('SSD')
    x_aa_tx_cpu = fields.Char('CPU')
    x_aa_tx_keyboard = fields.Char('Keyboard')
    x_aa_tx_colour = fields.Char('Colour')
    x_aa_tx_other_remarks = fields.Char('Other Remarks')
    x_aa_tx_product_qty = fields.Float('Quantity', compute='_custom_product_qty', store=True)
    x_aa_tx_tag_ids = fields.Char('TagID', default=lambda self: self.env['ir.sequence'].next_by_code('purchase.line.fields.lot.tagids') or '')

    @api.depends('quant_ids', 'quant_ids.quantity')
    def _custom_product_qty(self):
        for lot in self:
            # We only care for the quants in internal or transit locations.
            quants = lot.quant_ids.filtered(lambda q: q.location_id.usage == 'internal' or (q.location_id.usage == 'transit' and q.location_id.company_id))
            lot.x_aa_tx_product_qty = sum(quants.mapped('quantity'))

    @api.model
    def create(self, vals):
        res = super(StockProductionLot, self).create(vals)
        if res.product_id.product_template_variant_value_ids:
            for rec in res.product_id.product_template_variant_value_ids:
                if rec.attribute_id.with_context(lang='en_US').name == 'Storage':
                    res.x_aa_tx_storage = rec.product_attribute_value_id.name
                if rec.attribute_id.with_context(lang='en_US').name == 'Ram':
                    res.x_aa_tx_memory = rec.product_attribute_value_id.name
                if rec.attribute_id.with_context(lang='en_US').name == 'Colour':
                    res.x_aa_tx_colour = rec.product_attribute_value_id.name
                if rec.attribute_id.with_context(lang='en_US').name == 'Dual SIm':
                    res.x_aa_tx_dual_sim = rec.product_attribute_value_id.name
                if rec.attribute_id.with_context(lang='en_US').name == 'SSD':
                    res.x_aa_tx_ssd = rec.product_attribute_value_id.name
                if rec.attribute_id.with_context(lang='en_US').name == 'CPU':
                    res.x_aa_tx_cpu = rec.product_attribute_value_id.name
                if rec.attribute_id.with_context(lang='en_US').name == 'GPU':
                    res.x_aa_tx_graphics_card = rec.product_attribute_value_id.name
                if rec.attribute_id.with_context(lang='en_US').name == 'Grade':
                    res.x_aa_tx_grade = rec.product_attribute_value_id.with_context(lang='nl_NL').name
        return res