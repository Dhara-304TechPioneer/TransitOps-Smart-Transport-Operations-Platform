from odoo import models, fields

class FuelLog(models.Model):
    _name = 'transitops.fuel_log'
    _description = 'Vehicle Fuel Log'

    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True)
    liters = fields.Float(string='Liters', required=True)
    cost = fields.Float(string='Cost', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
