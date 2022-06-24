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

    x_aa_tx_grade = fields.Selection(related='product_id.x_aa_tx_grade')
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
    x_aa_tx_storage_id = fields.Many2one('mobile.storage', 'Storage', 
        domain="[('x_aa_tx_model_id', '=', x_aa_tx_model_id)]")
    x_aa_tx_graphics_card = fields.Selection([('test', 'TEST 1'), 
        ('test2', 'TEST 2')], string="Graphics Card")
    x_aa_tx_memory = fields.Selection([('test', 'TEST 1'), 
        ('test2', 'TEST 2')], string="Memory")
    x_aa_tx_keyboard = fields.Selection([('test', 'TEST 1'), 
        ('test2', 'TEST 2')], string="Keyboard")
    x_aa_tx_colour = fields.Selection([('black', 'Black'), 
        ('white', 'White'), 
        ('silver', 'Silver')], string="Colour")
    x_aa_tx_other_remarks = fields.Char('Other Remarks')
    x_aa_tx_product_qty = fields.Float('Quantity', compute='_custom_product_qty', store=True)


    @api.depends('quant_ids', 'quant_ids.quantity')
    def _custom_product_qty(self):
        for lot in self:
            # We only care for the quants in internal or transit locations.
            quants = lot.quant_ids.filtered(lambda q: q.location_id.usage == 'internal' or (q.location_id.usage == 'transit' and q.location_id.company_id))
            lot.x_aa_tx_product_qty = sum(quants.mapped('quantity'))
