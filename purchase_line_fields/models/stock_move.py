# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    x_aa_tx_grade = fields.Char("Grade")
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
    x_aa_tx_model_id = fields.Many2one('mobile.model', 'Model', domain="[('x_aa_tx_brand_id', '=', x_aa_tx_brand_id)]")
    x_aa_tx_storage_id = fields.Many2one('mobile.storage', 'Storage', domain="[('x_aa_tx_model_id', '=', x_aa_tx_model_id)]")
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

    @api.model
    def create(self, values):
        res = super(StockMove, self).create(values)
        if res.purchase_line_id.x_aa_tx_serial:
            res.write({
                'x_aa_tx_grade': res.purchase_line_id.x_aa_tx_grade,
                'x_aa_tx_battery_condition': res.purchase_line_id.x_aa_tx_battery_condition,
                'x_aa_tx_note': res.purchase_line_id.x_aa_tx_note,
                'x_aa_tx_booked': res.purchase_line_id.x_aa_tx_booked,
                'x_aa_tx_name': res.purchase_line_id.x_aa_tx_name,
                'x_aa_tx_extern_id': res.purchase_line_id.x_aa_tx_extern_id,
                'x_aa_tx_intern_id': res.purchase_line_id.x_aa_tx_intern_id,
                'x_aa_tx_imei': res.purchase_line_id.x_aa_tx_imei,
                'x_aa_tx_brand_id': res.purchase_line_id.x_aa_tx_brand_id.id,
                'x_aa_tx_model_id': res.purchase_line_id.x_aa_tx_model_id.id,
                'x_aa_tx_storage_id': res.purchase_line_id.x_aa_tx_storage_id.id,
                'x_aa_tx_graphics_card': res.purchase_line_id.x_aa_tx_graphics_card,
                'x_aa_tx_memory': res.purchase_line_id.x_aa_tx_memory,
                'x_aa_tx_keyboard': res.purchase_line_id.x_aa_tx_keyboard,
                'x_aa_tx_colour': res.purchase_line_id.x_aa_tx_colour,
                'x_aa_tx_other_remarks': res.purchase_line_id.x_aa_tx_other_remarks,
                })
        return res


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'    
    
    @api.model
    def create(self, values):
        res = super(StockMoveLine, self).create(values)
        if res.move_id.purchase_line_id.x_aa_tx_serial:
            res.write({
                'lot_name': res.move_id.purchase_line_id.x_aa_tx_serial,
                })
        return res
