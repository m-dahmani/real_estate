from odoo import models, fields


# 1.1python inheritance by classes(models.Model TransientModel AbstractModel )
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # 2.1model inheritance => extention model add field_rel not table in pgAdmin4(sale_order)
    property_id = fields.Many2one('property')

    # 1.2python inheritance Override methods  + CRUD Override
    def action_confirm(self):
        # res = super(SaleOrder, self).action_confirm()
        # or
        res = super().action_confirm()
        print("inside action_confirm method")
        return res
