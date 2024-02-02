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


class ProductProduct(models.Model):
    _inherit = 'product.product'

    #Stock
    stock_real = fields.Integer(string="Stock Real", compute='_product_total', help='muestral el stock real')
    # Sub products
    sub_product_line_ids = fields.One2many(related='bom_ids.bom_line_ids', string='Componentes', readonly=True)
    is_kit = fields.Boolean(string='Es un kit?', help='Este campo estará marcado si el SKU es combo o tiene lista de materiales', compute='_is_kit')
    component_list = fields.Boolean(string='Lista de componentes', help='Este campo estará marcado si el SKU es combo o tiene lista de materiales', compute='_id_yuju_kit')
    combo_qty = fields.Float(string='Total combos', help='Muestra la cantidad de combos que se pueden realizar con la lista de materiales actual', compute='_total_combos')
    #Calculated measures
    is_calculated_combo = fields.Boolean(string='Es combo', compute='calculated_measures')
    calculated_weight = fields.Float(string='Peso calculado', help='Muestra el cálculo del peso de los componentes del combo en kilogramos')
    calculated_volume = fields.Float(string='Volumen calculado', help='Muestra el cálculo del volumen de los componentes del combo, transforma centimetros cúbicos a Litros')

    #Function that evaluates if product is combo or kit
    @api.depends('is_kit')
    def _is_kit(self):
        self.ensure_one()
        _logger = logging.getLogger(__name__)

        if self.bom_count > 0:
            self.is_kit = True
        else:
            self.is_kit = False

    #@api.depends('is_kit')
    def _total_combos(self):
        if self.bom_count > 0 and self.yuju_kit:
            bom_line_ids = self.env['mrp.bom.line'].search([('bom_id', '=', self.yuju_kit.id)])
            for each in bom_line_ids:
                combo_calculation = each.combo_qty
                self.combo_qty = combo_calculation
        else:
            self.combo_qty = 0.0

    #@api.onchange('yuju_kit')
    def _id_yuju_kit(self):
        bom_line_ids = self.env['mrp.bom.line'].search([('bom_id', '=', self.yuju_kit.id)])
        self.component_list = True
        self.sub_product_line_ids = bom_line_ids

    #Calcula el peso y volumen para combos
    def calculated_measures(self):
        if self.bom_count > 0:
            weight_measures = []
            length_measures = []
            height_measures = []
            width_measures = []
            volume_calculation = []
            bom_line_ids = self.env['mrp.bom.line'].search([('bom_id', '=', self.yuju_kit.id)])
            product_ids = bom_line_ids['product_id']
            for product in product_ids:
                #Peso
                weight = product['packing_weight']
                weight_measures.append(weight)
                #Largo
                length = product['packing_length']
                length_measures.append(length)
                #Alto
                height = product['packing_height']
                height_measures.append(height)
                #Ancho
                width = product['packing_width']
                width_measures.append(width)

            max_length = max(length_measures)
            max_height = max(height_measures)
            sum_width = sum(width_measures)
            self.calculated_volume =  (max_length * max_height * sum_width) / 1000
            self.calculated_weight = sum(weight_measures)
            self.is_calculated_combo = True
        else:
            self.is_calculated_combo = False