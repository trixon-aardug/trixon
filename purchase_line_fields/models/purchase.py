# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    x_aa_tx_sku = fields.Char("SKU")
    x_aa_tx_serial = fields.Char("Serial")
    x_aa_tx_grade = fields.Selection(related='product_id.x_aa_tx_grade', store=True, readonly=True)
    x_aa_tx_battery_condition = fields.Char("Battery Condition")
    x_aa_tx_note = fields.Char("Note")
    x_aa_tx_is_sold = fields.Boolean(string='Sold', default=False)
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
    x_aa_tx_identifier = fields.Char('Identifier')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def create_serial_from_po(self):
        for record in self:
            for lines in record.order_line:
                if lines.x_aa_tx_serial:
                    create_lot = self.env['stock.production.lot'].create({
                        'name': lines.x_aa_tx_serial,
                        'company_id': self.company_id.id,
                        'product_id' : lines.product_id.id,
                        'x_aa_tx_grade' : lines.x_aa_tx_grade,
                        'x_aa_tx_battery_condition' : lines.x_aa_tx_battery_condition,
                        'x_aa_tx_note' : lines.x_aa_tx_note,
                        'x_aa_tx_booked' : lines.x_aa_tx_booked,
                        'x_aa_tx_name' : lines.x_aa_tx_name,
                        'x_aa_tx_extern_id' : lines.x_aa_tx_extern_id,
                        'x_aa_tx_intern_id' : lines.x_aa_tx_intern_id,
                        'x_aa_tx_imei' : lines.x_aa_tx_imei,
                        'x_aa_tx_brand_id' : lines.x_aa_tx_brand_id.id,
                        'x_aa_tx_model_id' : lines.x_aa_tx_model_id.id,
                        'x_aa_tx_storage_id' : lines.x_aa_tx_storage_id.id,
                        'x_aa_tx_graphics_card' : lines.x_aa_tx_graphics_card,
                        'x_aa_tx_memory' : lines.x_aa_tx_memory,
                        'x_aa_tx_keyboard' : lines.x_aa_tx_keyboard,
                        'x_aa_tx_colour' : lines.x_aa_tx_colour,
                        'x_aa_tx_other_remarks' : lines.x_aa_tx_other_remarks,
                        })
            return True


    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        self.create_serial_from_po()
        return res