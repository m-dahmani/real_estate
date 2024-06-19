from odoo import models


# 2.2model inheritance => inheritance model (attribute fields methods ...)
# add new table complet in pgAdmin4(client inheritance by owner)
class Client(models.Model):
    _name = 'client'
    _inherit = 'owner'
