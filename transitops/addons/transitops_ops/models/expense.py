from odoo import models, fields

class TransitOpsExpense(models.Model):
    _name = 'transitops.expense'
    _description = 'TransitOps Expense'

    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True)
    category = fields.Selection([
        ('toll', 'Toll'),
        ('other', 'Other')
    ], string='Category', required=True)
    amount = fields.Float(string='Amount', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
