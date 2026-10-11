from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class QueueReception(models.Model):
    _name = "queue.reception"
    _description = "Queue Reception"

    name = fields.Char(string="Reference", readonly=True, default=lambda self: _("New"))
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    counter_id = fields.Many2one("queue.counter", string="Counter", required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], default='draft', string="State")

    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if vals.get("name", _("New")) == _("New"):
    #             vals["name"] = (self.env["ir.sequence"].next_by_code("ksl.queue") or _("New"))
    #     return super().create(vals_list)

    def action_confirm(self):
        if self.name == _("New"):
            self.name = (self.env["ir.sequence"].next_by_code("ksl.queue") or _("New"))
        self.change_state('confirm')
        # import pdb
        # pdb.set_trace()
        # self.state = "confirm"

    def action_draft(self):
        self.change_state('draft')
        # self.state = "draft"

    def change_state(self, new_state):
        if self.is_allowed_transition(self.state, new_state):
            self.state = new_state  # confirm
        else:
            raise ValidationError(
                _("Moving from %s to %s is not allowed.")
                % (self.state, new_state)
            )

    #Parameters
    def is_allowed_transition(self, old_state, new_state):
        # Dictionary
        allowed_transitions = {
            'draft': ['confirm'],  # draft to confirm & confirm to draft
            'confirm': ['draft'],
        }
        return new_state in allowed_transitions.get(old_state, [])
