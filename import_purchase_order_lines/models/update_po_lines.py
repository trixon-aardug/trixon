# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _ ,exceptions
from datetime import datetime
from odoo.exceptions import Warning
import binascii
import tempfile
from tempfile import TemporaryFile
from odoo.exceptions import UserError, ValidationError
import logging
from odoo.tools import ustr
_logger = logging.getLogger(__name__)
import io

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


    
class update_po_line_wizard(models.TransientModel):
    _name='update.po.line.wizard'
    _description = "Update Purchase Order Line"

    purchase_order_file=fields.Binary(string="Select File")
    import_option = fields.Selection([('csv', 'CSV File'),('xls', 'XLS File')],string='Select',default='xls')
    import_prod_option = fields.Selection([('barcode', 'Barcode'),('code', 'Code'),('name', 'Name')],string='Import Product By ',default='code')
    product_details_option = fields.Selection([('from_product','Take Details From The Product'),('from_xls','Take Details From The XLS/CSV File'),('from_pricelist','Take Details With Adapted Pricelist')],default='from_xls')

    sample_option = fields.Selection([('csv', 'CSV'),('xls', 'XLS')],string='Sample Type',default='csv')
    down_samp_file = fields.Boolean(string='Download Sample Files')

    def update_pol(self):
        if self.import_option == 'csv':
            keys = ['identifier', 'code', 'quantity', 'uom','description', 'price', 'tax',
            'x_aa_tx_booked', 'x_aa_tx_sku', 'x_aa_tx_serial', 'x_aa_tx_grade', 'x_aa_tx_battery_condition',
            'x_aa_tx_note', 'x_aa_tx_name', 'x_aa_tx_brand_id', 'x_aa_tx_model_id', 'x_aa_tx_storage_id',
            'x_aa_tx_extern_id', 'x_aa_tx_intern_id', 'x_aa_tx_imei', 'x_aa_tx_graphics_card', 'x_aa_tx_memory',
            'x_aa_tx_keyboard', 'x_aa_tx_colour', 'x_aa_tx_other_remarks']
            try:
                csv_data = base64.b64decode(self.purchase_order_file)
                data_file = io.StringIO(csv_data.decode("utf-8"))
                data_file.seek(0)
                file_reader = []
                csv_reader = csv.reader(data_file, delimiter=',')
                file_reader.extend(csv_reader)
            except Exception:
                raise exceptions.ValidationError(_("Invalid file!"))
            values = {}
            for i in range(len(file_reader)):
                field = list(map(str, file_reader[i]))
                values = dict(zip(keys, field))
                if values:
                    if i == 0:
                        continue
                    else:
                        res = self.update_po_line(values)
        else:
            try:
                fp = tempfile.NamedTemporaryFile(delete= False,suffix=".xlsx")
                fp.write(binascii.a2b_base64(self.purchase_order_file))
                fp.seek(0)
                values = {}
                workbook = xlrd.open_workbook(fp.name)
                sheet = workbook.sheet_by_index(0)
            except Exception:
                raise exceptions.ValidationError(_("Invalid file!"))

            product_obj = self.env['product.product']
            for row_no in range(sheet.nrows):
                val = {}
                if row_no <= 0:
                    fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
                else:
                    line = list(map(lambda row:isinstance(row.value, bytes) and row.value.encode('utf-8') or ustr(row.value), sheet.row(row_no)))
                    if self.product_details_option == 'from_product':
                        values.update({
                                'code' : line[0].split('.')[0],
                                'quantity' : line[1]
                        })
                    elif self.product_details_option == 'from_xls':
                        values.update({
                           'identifier':line[0],
                           'code':line[1].split('.')[0],
                           'quantity':line[2],
                           'uom':line[3],
                           'description':line[4],
                           'price':line[5],
                           'tax':line[6],
                           'x_aa_tx_booked':line[7], 
                           'x_aa_tx_sku':line[8],
                           'x_aa_tx_serial':line[9],
                           # 'x_aa_tx_grade':line[10],
                           'x_aa_tx_battery_condition':line[11],
                           'x_aa_tx_note':line[12],
                           'x_aa_tx_name':line[13],
                           'x_aa_tx_brand_id':line[14],
                           'x_aa_tx_model_id':line[15],
                           'x_aa_tx_storage_id':line[16],
                           'x_aa_tx_extern_id':line[17],
                           'x_aa_tx_intern_id':line[18],
                           'x_aa_tx_imei':line[19],
                           'x_aa_tx_graphics_card':line[20],
                           'x_aa_tx_memory':line[21],
                           'x_aa_tx_keyboard':line[22],
                           'x_aa_tx_colour':line[23],
                           'x_aa_tx_other_remarks':line[24],
                            })
                    else:
                        values.update({
                                        'code' : line[0].split('.')[0],
                                        'quantity' : line[1],
                                    })                        

                    res = self.update_po_line(values)
        return res

    def update_po_line(self,values):
        purchase_order_brw=self.env['purchase.order'].browse(self._context.get('active_id'))
        current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        product=values.get('code')
        if values.get('x_aa_tx_brand_id'):
            brand_id = self.env['mobile.brand'].search(
                [('x_aa_tx_name', '=', values.get('x_aa_tx_brand_id'))])
        if values.get('x_aa_tx_model_id'):
            model_id = self.env['mobile.model'].search(
                [('x_aa_tx_name', '=', values.get('x_aa_tx_model_id')), 
                ('x_aa_tx_brand_id', '=', brand_id.id)])
        if values.get('x_aa_tx_storage_id'):
            storage_id = self.env['mobile.storage'].search(
                [('x_aa_tx_name', '=', values.get('x_aa_tx_storage_id')), 
                ('x_aa_tx_model_id', '=', model_id.id)])
        if self.product_details_option == 'from_xls':
            to_update_po_line = self.env['purchase.order.line'].search(
                [('order_id', '=', purchase_order_brw.id), ('x_aa_tx_identifier', '=', values.get('identifier'))])
            uom=values.get('uom')
            if self.import_prod_option == 'barcode':
              product_obj_search=self.env['product.product'].search([('barcode',  '=',values['code'])])
            elif self.import_prod_option == 'code':
                product_obj_search=self.env['product.product'].search([('default_code', '=',values['code'])])
            else:
                product_obj_search=self.env['product.product'].search([('name', '=',values['code'])])

            uom_obj_search=self.env['uom.uom'].search([('name','=',uom)])
            tax_id_lst=[]
            if values.get('tax'):
                if ';' in values.get('tax'):
                    tax_names = values.get('tax').split(';')
                    for name in tax_names:
                        tax = self.env['account.tax'].search([('name', '=', name), ('type_tax_use', '=', 'purchase')])
                        if not tax:
                            raise ValidationError(_('"%s" Tax not in your system') % name)
                        tax_id_lst.append(tax.id)

                elif ',' in values.get('tax'):
                    tax_names = values.get('tax').split(',')
                    for name in tax_names:
                        tax = self.env['account.tax'].search([('name', '=', name), ('type_tax_use', '=', 'purchase')])
                        if not tax:
                            raise ValidationError(_('"%s" Tax not in your system') % name)
                        tax_id_lst.append(tax.id)
                else:
                    tax_names = values.get('tax').split(',')
                    tax = self.env['account.tax'].search([('name', '=', tax_names), ('type_tax_use', '=', 'purchase')])
                    if not tax:
                        raise ValidationError(_('"%s" Tax not in your system') % tax_names)
                    tax_id_lst.append(tax.id)
            if not uom_obj_search:
                raise ValidationError(_('UOM "%s" is Not Available') % uom)

            if product_obj_search:
                product_id=product_obj_search[0]
            else:
                if self.import_prod_option == 'name':
                    if values.get('price'):
                        standard_price = float(values.get('price'))
                    else:
                        standard_price = False

                    product_id=self.env['product.product'].create({'name':product,'standard_price':standard_price})
                else:
                    raise ValidationError(_('%s product is not found" .\n If you want to create product then first select Import Product By Name option .') % values.get('code'))
            
            if values.get('quantity'):
                quantity = float(values.get('quantity'))
            else:
                quantity = False

            if purchase_order_brw.state == 'draft':
                if values.get('price'):
                    standard_price = float(values.get('price'))
                else:
                    standard_price = False
                to_update_po_line.write({
                    'product_id':product_id.id,
                    'name':values.get('description'),
                    'product_qty':quantity,
                    'product_uom':uom_obj_search.id or False,
                    'price_unit':standard_price,
                    'x_aa_tx_booked':values.get('x_aa_tx_booked'),
                    'x_aa_tx_sku':values.get('x_aa_tx_sku'),
                    'x_aa_tx_serial':values.get('x_aa_tx_serial'),
                    # 'x_aa_tx_grade':values.get('x_aa_tx_grade'),
                    'x_aa_tx_battery_condition':values.get('x_aa_tx_battery_condition'),
                    'x_aa_tx_note':values.get('x_aa_tx_note'),
                    'x_aa_tx_name':values.get('x_aa_tx_name'),
                    'x_aa_tx_brand_id':brand_id.id or False,
                    'x_aa_tx_model_id':model_id.id or False,
                    'x_aa_tx_storage_id':storage_id.id or False,
                    'x_aa_tx_extern_id':values.get('x_aa_tx_extern_id'),
                    'x_aa_tx_intern_id':values.get('x_aa_tx_intern_id'),
                    'x_aa_tx_imei':values.get('x_aa_tx_imei'),
                    'x_aa_tx_graphics_card':values.get('x_aa_tx_graphics_card'),
                    'x_aa_tx_memory':values.get('x_aa_tx_memory'),
                    'x_aa_tx_keyboard':values.get('x_aa_tx_keyboard'),
                    'x_aa_tx_colour':values.get('x_aa_tx_colour'),
                    'x_aa_tx_other_remarks':values.get('x_aa_tx_other_remarks'),
                    'x_aa_tx_identifier': 'TR.' + purchase_order_brw.name + '/' + values.get('x_aa_tx_intern_id'),
                    })
            elif purchase_order_brw.state == 'sent':
                to_update_po_line.write({
                        'product_id':product_id.id,
                        'name':product,
                        'product_qty':quantity,
                        'product_uom':uom_obj_search.id or False,
                        'price_unit':(values.get('price')),
                        'x_aa_tx_booked':values.get('x_aa_tx_booked'),
                        'x_aa_tx_sku':values.get('x_aa_tx_sku'),
                        'x_aa_tx_serial':values.get('x_aa_tx_serial'),
                        # 'x_aa_tx_grade':values.get('x_aa_tx_grade'),
                        'x_aa_tx_battery_condition':values.get('x_aa_tx_battery_condition'),
                        'x_aa_tx_note':values.get('x_aa_tx_note'),
                        'x_aa_tx_name':values.get('x_aa_tx_name'),
                        'x_aa_tx_brand_id':brand_id.id or False,
                        'x_aa_tx_model_id':model_id.id or False,
                        'x_aa_tx_storage_id':storage_id.id or False,
                        'x_aa_tx_extern_id':values.get('x_aa_tx_extern_id'),
                        'x_aa_tx_intern_id':values.get('x_aa_tx_intern_id'),
                        'x_aa_tx_imei':values.get('x_aa_tx_imei'),
                        'x_aa_tx_graphics_card':values.get('x_aa_tx_graphics_card'),
                        'x_aa_tx_memory':values.get('x_aa_tx_memory'),
                        'x_aa_tx_keyboard':values.get('x_aa_tx_keyboard'),
                        'x_aa_tx_colour':values.get('x_aa_tx_colour'),
                        'x_aa_tx_other_remarks':values.get('x_aa_tx_other_remarks'),
                        'x_aa_tx_identifier': 'TR.' + purchase_order_brw.name + '/' + values.get('x_aa_tx_intern_id'),
                        })
            elif purchase_order_brw.state != 'sent' or purchase_order_brw.state != 'draft':
                raise UserError(_('We cannot Update data in validated or confirmed order.'))
            if tax_id_lst:
                to_update_po_line.write({'taxes_id':([(6,0,tax_id_lst)])})   
        return True
    
    
    def download_auto_update(self):
        return {
             'type' : 'ir.actions.act_url',
             'url': '/web/binary/download_document?model=update.po.line.wizard&id=%s'%(self.id),
             'target': 'new',
             }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
