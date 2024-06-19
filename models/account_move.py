from odoo import models


# 1.1python inheritance by classes(models.Model TransientModel AbstractModel )
class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_do_something(self):
        print(self, "inside action_do_something method")
