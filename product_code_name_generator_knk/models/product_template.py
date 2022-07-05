# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import api, models, fields
from odoo.exceptions import UserError


class ProductCategory(models.Model):
    _inherit = 'product.category'

    attribute_ids = fields.One2many('attribute.line', 'category_id', string='Attributes')
    code = fields.Char()


class AttributeLine(models.Model):
    _name = 'attribute.line'

    category_id = fields.Many2one('product.category')
    sequence = fields.Integer(required=True, default=0)
    attribute = fields.Many2one('product.attribute', string='Attribute', required=True)
    display_code = fields.Boolean(string='Display Code')
    display_name = fields.Boolean(string='Display Name')


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    code = fields.Char()


class ProductAttributeLine(models.Model):
    _inherit = 'product.template.attribute.line'

    sequence = fields.Integer(required=True)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.onchange('categ_id')
    def onchange_categ_id(self):
        if self.categ_id:
            self.name = self.categ_id.name.split('/')[-1].strip()
            if self.categ_id.attribute_ids:
                self.attribute_line_ids = False
                self.attribute_line_ids = [(0, 0, {'sequence': i.sequence, 'attribute_id': i.attribute.id}) for i in self.categ_id.attribute_ids.sorted(lambda b: b.sequence)]

    def action_get_product_code(self):
        for product in self:
            for variant in product.product_variant_ids:
                variant.get_product_code()


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _default_name(self):
        if self.product_tmpl_id:
            self.name = self.product_tmpl_id.name

    name = fields.Char('Name', index=True, required=True, translate=True, default=_default_name)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            if vals.get('categ_id'):
                categ = self.env['product.category'].browse(int(vals.get('categ_id')))
                vals['name'] = categ.name if categ else ''
            if vals.get('product_tmpl_id'):
                product_tmpl = self.env['product.template'].browse(int(vals.get('product_tmpl_id')))
            vals['name'] = product_tmpl.name if product_tmpl else ''
        return super(ProductProduct, self).create(vals)

    def get_product_code(self):
        for product in self:
            code = name = ''
            attributes = []
            if product.product_template_attribute_value_ids:
                attributes = product.product_template_attribute_value_ids.mapped('attribute_id')
            if product.categ_id:
                code += product.categ_id.code or ''
                categ_name = product.categ_id.name.split('/')[-1].strip()
                name += categ_name
                if product.categ_id.attribute_ids:
                    for attr in product.categ_id.attribute_ids.sorted('sequence').filtered(lambda x: (x.display_code or x.display_name) and x.attribute in attributes):
                        for rec in product.product_template_attribute_value_ids:
                            if attr.display_code and rec.attribute_id == attr.attribute and rec.product_attribute_value_id:
                                code += rec.product_attribute_value_id.code or ''
                            if attr.display_name and rec.attribute_id == attr.attribute and rec.product_attribute_value_id:
                                attr_name = rec.product_attribute_value_id.display_name.split(': ')
                                name += ' ' + attr_name[0] + ' ' + attr_name[1] or ''
                else:
                    raise UserError('No attributes Selected for Category %s, Please Goto Category and add neccessary attributes to it.' % (product.categ_id.name))
            else:
                raise UserError('No Category is Selected, Please Choose a Relevant Category first.')
            if len(code) > 1 and code[-1] == '-':
                product.default_code = code[:-1]
            else:
                product.default_code = code
            product.name = name
        return True
