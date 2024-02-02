# -*- coding: utf-8 -*-
import base64
from odoo import api, fields, models, SUPERUSER_ID
from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime
from io import StringIO, BytesIO
import logging
import json
import requests


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    #Number of Packages
    packages_number = fields.Integer(string='Numero de Paquetes')
    #Product Measurements
    product_length = fields.Float(string='Largo producto', help="Largo del Producto en centimentros")
    product_height = fields.Float(string='Alto producto', help="Alto del Producto en centimentros")
    product_width = fields.Float(string='Ancho producto', help="Ancho del Producto en centimentros")
    product_weight = fields.Float(string='Peso producto', help="Peso del Producto en kilogramos")
    product_volume = fields.Float(string='Volumen producto', help="Volumen del Producto", compute='_volumen')
    #Packaging Measurements
    packing_length = fields.Float(string='Largo empaque', help="Largo del Empaque en centimentros")
    packing_height = fields.Float(string='Alto empaque', help="Alto del Empaque en centimentros")
    packing_width = fields.Float(string='Ancho empaque', help="Ancho del Empaque en centimentros")
    packing_weight = fields.Float(string='Peso empaque', help="Peso del Empaque en centimentros")
    #Comercial
    buyer = fields.Many2one('res.partner', string='Comprador responsable', help='Establece el comprador encargado de este SKU')
    owner = fields.Many2one('res.partner', string='Owner comercial', help='Establece el comercial responsable de este SKU')
    internal_category = fields.Many2one('internal.category', string='Categoría interna', help='Categoría interna para el equipo de SR')
    brand = fields.Many2one('product.brand', string='Marca', help='Marca a la que pertecene el SKU')
    #Logistics
    marketplace_codes = fields.Char(string='Códigos por marketplace', help='Códigos para comunicación con marketplace')
    provider_codes = fields.Char(string='Códigos por proveedor', help='Códigos del proveedor por SKU')
    nacional_import = fields.Selection([('importado', 'Importado'),
                                        ('nacional', 'Nacional')],
                                       string='Importacion/Nacional', help="Indica si el producto es importado o nacional")
    sold_out_industry = fields.Boolean(string='Agotado de industria', help='Producto que el proveedor reporta como agotado')
    approx_date_arrival = fields.Date(string='Fecha aprox de llegada', help='Posible fecha de resurtido por parte del proveedor para agotados de industria')
    #Product Status
    status = fields.Many2one('product.estatus', string='Estatus', help='Estatus del producto')
    substatus = fields.Many2one('product.subestatus', string='Subestatus', help='Subestatus del producto')
    status_sequence = fields.Char(related='status.sequence', string='Secuencia')
    status_subsequence = fields.Char(related='substatus.subsequence', string='Subsecuencia')
    #Seasonal and Period
    start_period = fields.Char(string='Inicio del periodo', help='Fecha/Mes en que inicia una estación o un Periodo para un SKU')
    end_period = fields.Char(string='Fin del periodo', help='Fecha/Mes en que finaliza una estación o un Periodo para un SKU')
    #Planning
    clasificacion_abc = fields.Char(string='Clasificación abc', help='Clasificación desarrollada por Planning')
    first_entry_date = fields.Date(string='Fecha primera entrada')
    last_entry_date = fields.Date(string='Fecha última entrada')
    first_departure_date = fields.Date(string='Fecha primera salida')
    last_departure_date = fields.Date(string='Fecha última salida')
    grava_iva = fields.Selection([('si', 'Si'),
                                  ('no', 'No')],
                                 string='Grava IVA', help='Identifica si el producto grava IVA')
    #Costs
    previous_cost = fields.Float(related='product_variant_id.previous_cost', string='Costo anterior', help='Muestra el costo anterior del producto')
    ps_cost = fields.Float(string='Costo PP', help="Campo con costo pronto pago. Aplica para descuentos financieros por pago")
    minimal_amount = fields.Float(string='Cantidad mínima', help='Cantidad de compra mínima por producto')
    #Substitute, Mirror and Variants
    substitute = fields.One2many('prod.relacionado', inverse_name='product_id', string='Productos', help='Muestra un producto que podría sustituir o reemplazar al seleccionado')
    #Stock
    stock_real = fields.Integer(related='product_variant_id.stock_real', string="Stock Real", help='muestral el stock real')
    #Markets
    mlm_ventas = fields.Char(string='Somos Reyes Ventas', help='Código MLM del SKU perteneciente a ventas')
    mlm_oficiales = fields.Char(string='Somos Reyes Oficiales', helpp='Código MLM del SKU perteneciente a oficiales')
    stock_full_ventas = fields.Integer(string='Stock Full Ventas', help='Stock de ventas')
    stock_full_oficiales = fields.Integer(string='Stock Full Oficiales', help='Stock de oficiales')
    full_api_ventas = fields.Boolean(string='Fullfilment Ventas API', help='Esquema del SKU de ventas mapeado por API')
    full_api_oficiales = fields.Boolean(string='Fullfilment Oficiales API', help='Esquema del SKU de oficiales mapeado por API')
    #Markets Manual
    full_ventas = fields.Boolean(string='Fullfilment Ventas', help='Esquema del SKU de ventas mapeado de forma manual')
    full_oficiales = fields.Boolean(string='Fullfilment Oficiales', help='Esquema del SKU de oficiales mapeado de forma manual')

    #Function that print the volume of product
    @api.depends('product_width','product_height','product_length')
    def _volumen(self):
        _logger = logging.getLogger(__name__)
        for rec in self:
            if rec.product_width > 0 and rec.product_height > 0 and rec.product_length > 0:
                rec.product_volume = round( (rec.product_width * rec.product_height * rec.product_length) / 5000,2)
            else:
                rec.product_volume = 0.00