from odoo import fields, models


class TransitOpsExpense(models.Model):
    _name = 'transitops.expense'
    _description = 'TransitOps Expense'
    _order = 'date desc, id desc'

    vehicle_id = fields.Many2one('transitops.vehicle', required=True, ondelete='restrict')
    category = fields.Selection([('toll', 'Toll'), ('other', 'Other')], default='other', required=True)
    amount = fields.Monetary(required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    date = fields.Date(default=fields.Date.today, required=True)
