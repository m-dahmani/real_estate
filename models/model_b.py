from odoo import models


# Create database temporel but after moment to remove it
class ModelB(models.TransientModel):
    _name = 'model.b'
