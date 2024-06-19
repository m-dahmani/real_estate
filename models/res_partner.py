from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_id = fields.Many2one('property')
    price = fields.Float(related='property_id.selling_price')  # , store=1, readonly=0
    # price = fields.Float(compute='_compute_price', store=1)

    # @api.depends('property_id')
    # def _compute_price(self):
    #     for rec in self:
    #         print(rec)
    #         print("inside _compute_price method")
    #         rec.price = rec.property_id.selling_price
