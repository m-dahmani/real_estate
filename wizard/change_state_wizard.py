from odoo import models, fields


class ChangeState(models.TransientModel):
    _name = 'change.state'

    property_id = fields.Many2one('property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending')
    ], default='draft')
    reason = fields.Char()

    def action_confirm(self):
        if self.property_id.state == 'closed':
            print("inside confirm action")
            self.property_id.state = self.state  # the value to choose it the user
            self.property_id.create_history_record('closed', self.state, self.reason)



