# -*- coding: utf-8 -*-
{
    'name': "Modificaciones Formulario de Producto",

    'summary': """
        Modificaciones al template del producto para uso general e interno""",

    'description': """
        Este módulo agrega diferentes modificaciones y campos al formulario del producto
        
        -Medidas de empaque (Largo, alto, ancho, peso)
        -Medidas de producto (Largo, alto, ancho, peso)
        -Catálogos de marketplace
        -Categoría por MP
        -Importación/Nacional
        -Esquema logístico original por canal/tienda
        -Comprador
        -Agotado de industria
        -Producto sustituto/espejo
        -Comprador
        -Costo anterior/reposición/último pagado
        -Códigos por Marketplace/Proveedor
        -Agrava IVA
        -Fechas de primera y última salida
        -Planning
        -Esquema logístico
    """,

    'author': "Wonderbrands",
    'website': "https://www.wonderbrands.co",
    'license': 'LGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '16.0',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'product',
                'sale',
                'stock',
                ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/product_supplierinfo_views.xml',
        'views/product_template_views.xml',
        # 'views/templates.xml',
        'views/product_views.xml',
        'views/mrp_bom_line_views.xml',
        'data/internal.category.csv',
        'data/product.brand.csv',
    ],
}