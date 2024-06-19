from odoo import models, fields


class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(required=1)
    phone = fields.Char()
    address = fields.Char()
    property_ids = fields.One2many(comodel_name='property', inverse_name='owner_id')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is already exist!')
    ]
