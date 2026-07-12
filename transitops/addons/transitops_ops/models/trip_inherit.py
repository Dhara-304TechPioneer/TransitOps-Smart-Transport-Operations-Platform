from odoo import models, fields, api

class TransitOpsTripInherit(models.Model):
    _inherit = 'transitops.trip'

    fuel_efficiency = fields.Float(string='Fuel Efficiency (km/L)', compute='_compute_fuel_efficiency', store=True)

    @api.depends('planned_distance_km', 'fuel_consumed')
    def _compute_fuel_efficiency(self):
        for trip in self:
            if trip.fuel_consumed and trip.fuel_consumed > 0:
                trip.fuel_efficiency = trip.planned_distance_km / trip.fuel_consumed
            else:
                trip.fuel_efficiency = 0.0
