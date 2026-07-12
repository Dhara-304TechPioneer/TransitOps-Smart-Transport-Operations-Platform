from odoo import fields, models, _
from odoo.exceptions import UserError, ValidationError


class TransitOpsTrip(models.Model):
    _name = 'transitops.trip'
    _description = 'TransitOps Trip'
    _order = 'id desc'

    source = fields.Char(required=True)
    destination = fields.Char(required=True)
    vehicle_id = fields.Many2one('transitops.vehicle', required=True, ondelete='restrict')
    driver_id = fields.Many2one('transitops.driver', required=True, ondelete='restrict')
    cargo_weight_kg = fields.Float(string='Cargo Weight (kg)', required=True)
    planned_distance_km = fields.Float(string='Planned Distance (km)')
    fuel_consumed = fields.Float(string='Fuel Consumed (L)')
    final_odometer = fields.Float(string='Final Odometer (km)')
    revenue = fields.Monetary(string='Revenue')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection([('draft', 'Draft'), ('dispatched', 'Dispatched'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='draft', required=True)
    fuel_efficiency = fields.Float(compute='_compute_fuel_efficiency', string='Fuel Efficiency (km/L)')

    def _compute_fuel_efficiency(self):
        for trip in self:
            trip.fuel_efficiency = trip.planned_distance_km / trip.fuel_consumed if trip.fuel_consumed else 0

    def _validate_dispatch(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft trips can be dispatched.'))
        if self.vehicle_id.status != 'available':
            raise ValidationError(_('Vehicle %s is not available.') % self.vehicle_id.name)
        if self.driver_id.status != 'available':
            raise ValidationError(_('Driver %s is not available.') % self.driver_id.name)
        if not self.driver_id.license_expiry or self.driver_id.license_expiry < fields.Date.today():
            raise ValidationError(_('Driver license is expired or missing.'))
        if self.cargo_weight_kg > self.vehicle_id.max_load_kg:
            raise ValidationError(_('Cargo weight exceeds the vehicle maximum load.'))

    def action_dispatch(self):
        for trip in self:
            trip._validate_dispatch()
            trip.vehicle_id.status = 'on_trip'
            trip.driver_id.status = 'on_trip'
            trip.state = 'dispatched'
        return True

    def action_complete(self):
        for trip in self:
            if trip.state != 'dispatched':
                raise UserError(_('Only dispatched trips can be completed.'))
            trip.vehicle_id.status = 'available'
            trip.driver_id.status = 'available'
            if trip.final_odometer:
                trip.vehicle_id.odometer = trip.final_odometer
            trip.state = 'completed'
        return True

    def action_cancel(self):
        for trip in self:
            if trip.state == 'dispatched':
                trip.vehicle_id.status = 'available'
                trip.driver_id.status = 'available'
            if trip.state not in ('draft', 'dispatched'):
                raise UserError(_('Only draft or dispatched trips can be cancelled.'))
            trip.state = 'cancelled'
        return True
