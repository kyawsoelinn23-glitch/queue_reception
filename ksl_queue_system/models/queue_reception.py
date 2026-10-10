from odoo import models, fields, api, _


class QueueReception(models.Model):
    _name = "queue.reception"
    _description = "Queue Reception"

    name = fields.Char(string="Name", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner")
    counter_id = fields.Many2one("queue.counter", string="Counter")