"""Property Model"""
# flake8: noqa
# pylint: disable=line-too-long
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = "property"
    _description = "Property"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    ref = fields.Char(readonly=1, default="New")
    name = fields.Char(required=1, default="Property", size=50, translate=True)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float(digits=(0, 4))
    selling_price = fields.Float()
    diff = fields.Float(compute="_compute_diff")  # , store=1, readonly=0
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(groups="app_one.group_property_manager")
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
             ("north", "North"),
             ("south", "South"),
             ("east", "East"),
             ("west", "West")
        ],
        default="north",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("pending", "Pending"),
            ("sold", "Sold"),
            ("closed", "Closed"),
        ],
        default="draft",
    )
    owner_id = fields.Many2one("owner")
    tag_ids = fields.Many2many("tag")
    # owner_address related has m type of owner_id.address
    owner_address = fields.Char(related="owner_id.address", readonly=0)  # , store=1
    owner_phone = fields.Char(related="owner_id.phone", readonly=0)  # , store=1
    # Archiving / Unarchiving Technique
    active = fields.Boolean(default=True)

    create_time = fields.Datetime(default=fields.Datetime.now)
    next_time = fields.Datetime(compute="_compute_next_time")

    _sql_constraints = [
        ("unique_name", 'unique("name")', "This name is already exist !")
        # ('check_field', 'check("field")', 'message for the field')
        # ('exclude_field', 'exclude("field")', 'message for the field')
    ]

    line_ids = fields.One2many(comodel_name="property.line", inverse_name="property_id")

    @api.depends("create_time")
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False

    # it depends include views_fields & model_fields & related_fields return rec property(1,)
    @api.depends("expected_price", "selling_price", "owner_id.address")
    def _compute_diff(self):
        for rec in self:
            print(rec)
            print("inside _compute_diff method")
            rec.diff = rec.expected_price - rec.selling_price

    # it depends include views_fields only return sudo rec property(<NewId origin=1>,)
    @api.onchange("expected_price")
    def _onchange_expected_price(self):
        for rec in self:
            print(rec)
            print("inside _onchange_expected_price method")
            warning = {
                "title": "Warning",
                "message": "Negative Value",
                "type": "notification",
            }
            return {"warning": warning}

    @api.constrains("bedrooms")
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError("Please add valid number of bedrooms")

    def action_draft(self):
        for rec in self:
            rec.create_history_record(old_state=rec.state, new_state="draft", reason="")
            print("inside draft action")
            # rec.state == 'draft'
            rec.write({"state": "draft"})

    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, "pending")
            print("inside pending action")
            # rec.state == 'pending'
            rec.write({"state": "pending"})

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, "sold")
            print("inside sold action")
            # rec.state == 'sold'
            rec.write({"state": "sold"})

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, "closed")
            rec.write({"state": "closed"})

    def check_expected_selling_date(self):
        print(self)
        print("inside check_expected_selling_date method")
        property_ids = self.search([])
        print(property_ids)
        for rec in property_ids:
            print(rec)
            if (
                rec.expected_selling_date
                and rec.expected_selling_date < fields.Date.today()
            ):
                rec.is_late = True

    # CRUD OPERATION Override
    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(Property, self).create(vals) # or
    #     # res = super().create(vals)
    #     print("inside create method")
    #     return res
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     print("inside search method")
    #     return res
    #
    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     print("inside write method")
    #     return res
    #
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print("inside unlink method")
    #     return res

    def action(self):
        print(self.env)
        # return all data of object user and company
        print(self.env.user)
        print(self.env.user.login)
        print(self.env.user.name)
        print(self.env.user.id)
        # print(self.env.user.id==self.env.uid)
        print(self.env.uid)
        print(self.env.company)
        # print(self.env.company.field)
        print(self.env.company.name)
        print(self.env.company.id)
        print(self.env.context)
        print(self.env.cr)  # sql_query
        print(
            self.env["owner"].create(
                {
                    "name": "One record",
                    "phone": "0111111111111",
                    "address": "hay massira",
                }
            )
        )  # call create of the another model of the project self.env['model_name']

        print(
            self.env["owner"].search([])
        )  # call any method of the another model of the project with env
        # [] is empty => return all records

        # [('name_field', 'operators', 'value_field'),
        # ('name_field', '!=', 'value_field'),
        #  ('name_field', 'in', ['value_field', 'value_field']),
        # ('name_field', 'in', ('value_field', 'value_field')),
        # ('name_field', 'like', 'Property1') return => Property1 Property12 Property1_
        # ('name_field', 'ilike', 'Property1') return => Property1 Property12 Property1_ property1
        #  ]
        #         [('name', '=', 'Property1')]
        print(self.env["property"].search([("name", "=", "Property1")]))
        print(self.env["property"].search([("name", "!=", "Property1")]))
        print(
            self.env["property"].search(
                [("name", "=", "Property1"), ("postcode", "!=", "1234")]
            )
        )  # default 'and'
        print(
            self.env["property"].search(
                ["&", ("name", "=", "Property1"), ("postcode", "!=", "1234")]
            )
        )  # 'and'
        print(
            self.env["property"].search(
                ["|", ("name", "=", "Property1"), ("postcode", "!=", "1234")]
            )
        )  # 'or'
        print(
            self.env["property"].search(
                ["!", ("name", "=", "Property1"), ("postcode", "=", "1234")]
            )
        )  # 'not'

    @api.model
    def create(self, vals):
        # res = super(Property, self).create(vals)
        res = super().create(vals)
        if res.ref == "New":
            res.ref = self.env["ir.sequence"].next_by_code("property_seq")
        return res

    def create_history_record(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env["property.history"].create(
                {
                    "user_id": rec.env.uid,
                    "property_id": rec.id,
                    "old_state": old_state,
                    "new_state": new_state,
                    "reason": reason or "",
                    # command.create magic_tuples => create record by another model_name for fields.One2many
                    # not same from view
                    # [(.create, create_rec_not_exist, {'field': line.field, 'field': line.field}) for line in
                    # rec.line_ids]
                    "line_ids": [
                        (0, 0, {"description": line.description, "area": line.area})
                        for line in rec.line_ids
                    ],
                }
            )

    def action_open_change_state_wizard(self):
        # I need an action exist in model ir.actions.actions by method _for_xml_id
        # that I can open change_state_wizard_action
        action = self.env["ir.actions.actions"]._for_xml_id(
            "app_one.change_state_wizard_action"
        )
        # I need value default for property_id that exist in model change.state.wizard
        # to aplay new state in this property_id
        # that I have already its ID
        # once I open popup window set the value default property_id == record
        # or I open server action through my window
        action["context"] = {"default_property_id": self.id}
        return action

    def action_open_related_owner(self):
        print("inside action_open_related_owner action")
        # I need an action that I can open the owner's action,
        action = self.env["ir.actions.actions"]._for_xml_id("app_one.owner_action")
        # I need to open the form view
        view_id = self.env.ref("app_one.owner_view_form").id
        action["views"] = [[view_id, "form"]]  # [[False, 'form']]
        # and I also need the res_id to open the owner's ID that I can open
        action["res_id"] = self.owner_id.id  # self.push_reminder_posts[0].id
        return action


#     BedroomLine(models.Model)
class PropertyLine(models.Model):
    _name = "property.line"

    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one("property")
