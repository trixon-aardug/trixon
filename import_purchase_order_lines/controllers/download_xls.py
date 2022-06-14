# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition
import base64
import os, os.path
import csv
from os import listdir
import sys

class Download_xls(http.Controller):
    
    @http.route('/web/binary/download_document', type='http', auth="public")
    def download_document(self,model,id, **kw):
        Model = request.env[model]
        res = Model.browse(int(id))
        if Model._name == 'import.po.line.wizard':
            if res.sample_option == 'xls':
                invoice_xls = request.env['ir.attachment'].search([('name','=','purchase_order_line.xls')])
                filecontent = invoice_xls.datas
                filename = 'Purchase Order Line.xls'
                filecontent = base64.b64decode(filecontent)
            elif res.sample_option == 'csv':
                invoice_xls = request.env['ir.attachment'].search([('name','=','purchase_order_line.csv')])
                filecontent = invoice_xls.datas
                filename = 'Purchase Order Line.csv'
                filecontent = base64.b64decode(filecontent)

        elif Model._name == 'update.po.line.wizard':
            if res.sample_option == 'csv':
                invoice_xls = request.env['ir.attachment'].search([('name','=','purchase_order_line_update.csv')])
                filecontent = invoice_xls.datas
                filename = 'Purchase Order Line Update.csv'
                filecontent = base64.b64decode(filecontent)
            elif res.sample_option == 'xls':
                invoice_xls = request.env['ir.attachment'].search([('name','=','purchase_order_line_update.xls')])
                filecontent = invoice_xls.datas
                filename = 'Purchase Order Line Update.xls'
                filecontent = base64.b64decode(filecontent)

        return request.make_response(filecontent,
            [('Content-Type', 'application/octet-stream'),
            ('Content-Disposition', content_disposition(filename))])