# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    x_aa_tx_grade = fields.Char('Grade')
