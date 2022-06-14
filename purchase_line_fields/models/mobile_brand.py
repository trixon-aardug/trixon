# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models


class MobileBrand(models.Model):
    _name = "mobile.brand"
    _description = "Mobile Brand"
    _rec_name = 'x_aa_tx_name'

    x_aa_tx_name = fields.Char('Name')
    x_aa_tx_models = fields.One2many('mobile.model', 'x_aa_tx_brand_id', string='Brand Lines')