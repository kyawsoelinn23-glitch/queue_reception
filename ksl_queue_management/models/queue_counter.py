from odoo import api, fields, models

class QueueCounter(models.Model):
    _name = "queue.counter"
    _description = "Queue Counter"

    name = fields.Char(required=True)
