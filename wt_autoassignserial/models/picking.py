# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_assign(self):
        res = super(StockPicking, self).action_assign()
        self.assign_sale_lot()
        return res

    def assign_sale_lot(self):
        for record in self:
            for move in record.move_lines.filtered(
                lambda mv: mv.sale_line_id and mv.sale_line_id.lot_ids
            ):
                for lot in move.sale_line_id.lot_ids:
                    for line in move.move_line_ids:
                        if not line.qty_done:
                            line.lot_id = lot.id
                            line.qty_done = 1
                            break
