from odoo import models, fields


# Reserved Field Names & Archiving / Unarchiving Technique
class Building(models.Model):
    _name = 'building'
    _description = 'Building Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # _rec_name = 'code' # id doesnt field_name because it has value id by default
    # if field_name exist _rec_name==name by default sauf _rec_name== other_field

    # Reserved Field Names
    name = fields.Char(translate=True)
    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()
    # Archiving / Unarchiving Technique
    active = fields.Boolean(default=True)
