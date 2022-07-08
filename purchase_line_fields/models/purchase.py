# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    x_aa_tx_sku = fields.Char("SKU")
    x_aa_tx_serial = fields.Char("Serial")
    x_aa_tx_grade = fields.Char('Grade')
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
    x_aa_tx_storage = fields.Char('Storage')
    x_aa_tx_graphics_card = fields.Char('Graphics Card')
    x_aa_tx_memory = fields.Char('Memory')
    x_aa_tx_dual_sim = fields.Char('Dual Sim')
    x_aa_tx_ssd = fields.Char('SSD')
    x_aa_tx_cpu = fields.Char('CPU')
    x_aa_tx_keyboard = fields.Char('Keyboard')
    x_aa_tx_colour = fields.Char('Colour')
    x_aa_tx_other_remarks = fields.Char('Other Remarks')
    x_aa_tx_identifier = fields.Char('Identifier')
    x_aa_tx_tag_ids = fields.Char('TagID', compute='_compute_tagfrom_lots')


    def _compute_tagfrom_lots(self):
        for line in self:
            find_lot_id = self.env['stock.production.lot'].search(
                [('name', '=', line.x_aa_tx_serial),
                ('product_id', '=', line.product_id.id)], limit=1)
            if find_lot_id:
                line.x_aa_tx_tag_ids = find_lot_id.x_aa_tx_tag_ids
            else:
                line.x_aa_tx_tag_ids = ''

    @api.model
    def create(self, vals):
        res = super(PurchaseOrderLine, self).create(vals)
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

    def write(self, vals):
        if 'product_id' in vals:
            set_storage = False
            set_memory = False
            set_colour = False
            set_dualsim = False
            set_ssd = False
            set_cpu = False
            set_gpu = False
            set_grade = False
            new_product_id = self.env['product.product'].browse(vals.get('product_id'))
            for line in new_product_id.product_template_variant_value_ids:
                if line.attribute_id.with_context(lang='en_US').name == 'Storage':
                    vals['x_aa_tx_storage'] = line.product_attribute_value_id.name
                    set_storage = True
                else:
                    if not set_storage:
                        vals['x_aa_tx_storage'] = ''
                if line.attribute_id.with_context(lang='en_US').name == 'Ram':
                    vals['x_aa_tx_memory'] = line.product_attribute_value_id.name
                    set_memory = True
                else:
                    if not set_memory:
                        vals['x_aa_tx_memory'] = ''
                if line.attribute_id.with_context(lang='en_US').name == 'Colour':
                    vals['x_aa_tx_colour'] = line.product_attribute_value_id.name
                    set_colour = True
                else:
                    if not set_colour:
                        vals['x_aa_tx_colour'] = ''
                if line.attribute_id.with_context(lang='en_US').name == 'Dual SIm':
                    vals['x_aa_tx_dual_sim'] = line.product_attribute_value_id.name
                    set_dualsim = True
                else:
                    if not set_dualsim:
                        vals['x_aa_tx_dual_sim'] = ''
                if line.attribute_id.with_context(lang='en_US').name == 'SSD':
                    vals['x_aa_tx_ssd'] = line.product_attribute_value_id.name
                    set_ssd = True
                else:
                    if not set_ssd:
                        vals['x_aa_tx_ssd'] = ''
                if line.attribute_id.with_context(lang='en_US').name == 'CPU':
                    vals['x_aa_tx_cpu'] = line.product_attribute_value_id.name
                    set_cpu = True
                else:
                    if not set_cpu:
                        vals['x_aa_tx_cpu'] = ''
                if line.attribute_id.with_context(lang='en_US').name == 'GPU':
                    vals['x_aa_tx_graphics_card'] = line.product_attribute_value_id.name
                    set_gpu = True
                else:
                    if not set_gpu:
                        vals['x_aa_tx_graphics_card'] = ''
                if line.attribute_id.with_context(lang='en_US').name == 'Grade':
                    vals['x_aa_tx_grade'] = line.product_attribute_value_id.with_context(lang='nl_NL').name
                    set_grade = True
                else:
                    if not set_grade:
                        vals['x_aa_tx_grade'] = ''
        return super(PurchaseOrderLine, self).write(vals)

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
                        'x_aa_tx_storage' : lines.x_aa_tx_storage,
                        'x_aa_tx_graphics_card' : lines.x_aa_tx_graphics_card,
                        'x_aa_tx_memory' : lines.x_aa_tx_memory,
                        'x_aa_tx_dual_sim' : lines.x_aa_tx_dual_sim,
                        'x_aa_tx_ssd' : lines.x_aa_tx_ssd,
                        'x_aa_tx_cpu' : lines.x_aa_tx_cpu,
                        'x_aa_tx_keyboard' : lines.x_aa_tx_keyboard,
                        'x_aa_tx_colour' : lines.x_aa_tx_colour,
                        'x_aa_tx_other_remarks' : lines.x_aa_tx_other_remarks,
                        })
            return True


    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        self.create_serial_from_po()
        return res
