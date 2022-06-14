# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for record in self:
            if any(
                record.order_line.filtered(
                    lambda x: x.lot_ids and len(x.lot_ids) != x.product_uom_qty
                )
            ):
                raise Warning(_("Please ensure product qty is equal to lots."))
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    serial = fields.Char(string="Scan Serial No.")
    lot_ids = fields.Many2many(
        "stock.production.lot",
        "rel_lot_product",
        "lot_id",
        "product_id",
        string="Lot/Serial",
    )

    @api.onchange("serial")
    def onchange_serial(self):
        if self.serial:
            lot = self.env["stock.production.lot"]
            if not self.product_id:
                lot = lot.search([("name", "=", self.serial)])
            else:
                lot = lot.search(
                    [
                        ("name", "=", self.serial),
                        ("product_id", "=", self.product_id.id),
                    ]
                )
            if lot:
                if lot.product_qty == 0.0:
                    self.serial = ""
                    raise Warning(_("Sorry! Serial number is already processed!"))
                else:
                    self.product_id = lot.product_id.id
                    self.lot_ids = [(4, lot.id)]
                    self.serial = ""
            else:
                self.serial = ""
                raise Warning(_("Sorry! No serial number found in system."))

    @api.onchange("lot_ids")
    def onchange_lot_ids(self):
        self.product_uom_qty = len(self.lot_ids)
