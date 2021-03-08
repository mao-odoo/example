# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api,fields,models,_

class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount_type = fields.Selection([('percentage',' Percentage '),('amount','Amount')],string = 'Discount Type' , default='percentage')
    percentage =  fields.Float(string = "Discount Percentage")
    amount =  fields.Float(string = "Discount Amount")
    amount_untaxed = fields.Float(string = " Amount untaxed" ,compute="_amount_all",store=True)
    
    #compute method of sale order
    @api.depends('order_line.price_total','discount_type','percentage','amount')
    def _amount_all(self):
        result = super(SaleOrder, self)._amount_all()
        """
        Compute the total amounts of the SO.
        """
        for rec in self:
            if rec.discount_type == 'amount':
                rec.amount_untaxed=rec.amount_untaxed - rec.amount
            else:
                if rec.amount_untaxed and rec.percentage:
                    discount=rec.amount_untaxed * rec.percentage/100
                    rec.amount_untaxed=rec.amount_untaxed - discount
                    rec.amount_total+=rec.amount_untaxed 
        rec.update({
                'amount_total': rec.amount_untaxed + rec.amount_tax,
            })
        return result


