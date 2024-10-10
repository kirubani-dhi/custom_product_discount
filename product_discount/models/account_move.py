from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _prepare_invoice_line(self, line):
        line_data = super(AccountMove, self)._prepare_invoice_line(line)
        if line.product_id.discount_percentage > 0:
            line_data['price_unit'] = line.product_id.discounted_price
        return line_data