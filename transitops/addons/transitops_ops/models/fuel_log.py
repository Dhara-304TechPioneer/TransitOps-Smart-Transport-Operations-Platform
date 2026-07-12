from odoo import fields, models


class TransitOpsFuelLog(models.Model):
    _name = 'transitops.fuel_log'
    _description = 'TransitOps Fuel Log'
    _order = 'date desc, id desc'

    vehicle_id = fields.Many2one('transitops.vehicle', required=True, ondelete='restrict')
    liters = fields.Float(required=True)
    cost = fields.Monetary(required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    date = fields.Date(default=fields.Date.today, required=True)
    _sql_constraints = [('fuel_liters_positive', 'CHECK(liters > 0)', 'Liters must be greater than zero.')]
