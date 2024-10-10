from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            tax_results = self.env['account.tax'].with_company(line.company_id)._compute_taxes([
                line._convert_to_tax_base_line_dict()
            ])
            totals = list(tax_results['totals'].values())[0]
            # update discount value
            if line.product_id.product_tmpl_id.discount_percentage > 0:
                price = line.product_id.product_tmpl_id.discounted_price
            else:
                price = totals['amount_untaxed']
            amount_untaxed = price
            amount_tax = totals['amount_tax']

            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': amount_untaxed + amount_tax,
                'price_unit': price
            })

    @api.depends('price_subtotal', 'product_uom_qty')
    def _compute_price_reduce_taxexcl(self):
        for line in self:
            # update discount value
            if line.product_id.product_tmpl_id.discount_percentage > 0:
                price = line.product_id.product_tmpl_id.discounted_price
            else:
                price = line.price_subtotal
            line.price_reduce_taxexcl = price / line.product_uom_qty if line.product_uom_qty else 0.0

    @api.depends('price_total', 'product_uom_qty')
    def _compute_price_reduce_taxinc(self):
        for line in self:
            # update discount value
            if line.product_id.product_tmpl_id.discount_percentage > 0:
                price = line.product_id.product_tmpl_id.discounted_price
            else:
                price = line.price_subtotal
            line.price_reduce_taxinc = price / line.product_uom_qty if line.product_uom_qty else 0.0
