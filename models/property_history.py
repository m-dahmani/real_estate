from odoo import models, fields


class PropertyHistory(models.Model):
    _name = 'property.history'
    _description = 'Property History'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property')
    old_state = fields.Char()
    new_state = fields.Char()
    reason = fields.Char()

    line_ids = fields.One2many(comodel_name='property.history.line', inverse_name='history_id')


class PropertyHistoryLine(models.Model):
    _name = 'property.history.line'

    history_id = fields.Many2one('property.history')
    area = fields.Float()
    description = fields.Char()
