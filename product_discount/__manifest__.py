{
    'name': 'Product Discount',
    'version': '1.0',
    'author': 'Kiruba',
    'depends': ['product', 'website_sale'],
    'data': [
        'views/product_template_views.xml',
        'views/website_sale_templates.xml',
    ],
    "assets": {
        "web._assets_primary_variables": [
            "/product_discount/static/src/scss/website_sale_discount.scss"
        ]
    },
    'installable': True,
    'application': False,
}
