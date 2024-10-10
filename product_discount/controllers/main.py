from odoo import http
from odoo.http import request
import json

class WebsiteSale(http.Controller):

    @http.route(['/shop/cart/update'], type='json', auth='public', methods=['POST'], website=True)
    def cart_update(self, **kwargs):
        # Call the original method to update cart
        response = super(WebsiteSale, self).cart_update(**kwargs)

        # Update cart line item prices with discounted prices
        cart = request.website.sale_get_order()
        if cart:
            for line in cart.order_line:
                if line.product_id.discount_percentage > 0:
                    line.price_unit = line.product_id.discounted_price

        return response

    @http.route(['/shop/confirm_order'], type='http', auth='public', methods=['POST'], website=True)
    def confirm_order(self, **kwargs):
        # Call the original method
        order = super(WebsiteSale, self).confirm_order(**kwargs)

        # Update the order lines with discounted prices
        for line in order.order_line:
            if line.product_id.discount_percentage > 0:
                line.price_unit = line.product_id.discounted_price

        return request.redirect('/shop/confirmation')

class WebsiteSaleVariantController(http.Controller):

    @http.route('/website_sale/get_combination_info', type='json', auth='public', methods=['POST'], website=True)
    def get_combination_info_website(
        self, product_template_id, product_id, combination, add_qty, parent_combination=None,
        **kwargs
    ):
        product_template = request.env['product.template'].browse(
            product_template_id and int(product_template_id))

        combination_info = product_template._get_combination_info(
            combination=request.env['product.template.attribute.value'].browse(combination),
            product_id=product_id and int(product_id),
            add_qty=add_qty and float(add_qty) or 1.0,
            parent_combination=request.env['product.template.attribute.value'].browse(parent_combination),
        )

        # Pop data only computed to ease server-side computations.
        for key in ('product_taxes', 'taxes', 'currency', 'date'):
            combination_info.pop(key)

        if request.website.product_page_image_width != 'none' and not request.env.context.get('website_sale_no_images', False):
            combination_info['carousel'] = request.env['ir.ui.view']._render_template(
                'website_sale.shop_product_images',
                values={
                    'product': product_template,
                    'product_variant': request.env['product.product'].browse(combination_info['product_id']),
                    'website': request.env['website'].get_current_website(),
                },
            )
        if product_template.discount_percentage > 0:
            combination_info['price'] = product_template.discounted_price
            combination_info['list_price'] = product_template.discounted_price
        return combination_info
