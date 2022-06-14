# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models


class MobileModel(models.Model):
    _name = "mobile.model"
    _description = "Mobile Model"
    _rec_name = 'x_aa_tx_name'
    
    x_aa_tx_name = fields.Char('Name')
    x_aa_tx_brand_id = fields.Many2one('mobile.brand', 'Brand')
    x_aa_tx_storage = fields.One2many('mobile.storage', 'x_aa_tx_model_id', string='Storage Lines')