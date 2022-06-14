# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models


class MobileStorage(models.Model):
    _name = "mobile.storage"
    _description = "Mobile Model storage"
    _rec_name = 'x_aa_tx_name'
    
    x_aa_tx_name = fields.Char('Name')
    x_aa_tx_model_id = fields.Many2one('mobile.model', 'Model')