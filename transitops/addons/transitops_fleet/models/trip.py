from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TransitOpsTrip(models.Model):
    _name = 'transitops.trip'
    _description = 'TransitOps Trip'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    source = fields.Char(string='Source', required=True, tracking=True)
    destination = fields.Char(string='Destination', required=True, tracking=True)
    
    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True, tracking=True)
    driver_id = fields.Many2one('transitops.driver', string='Driver', required=True, tracking=True)
    
    cargo_weight_kg = fields.Float(string='Cargo Weight (kg)', required=True, tracking=True)
    planned_distance_km = fields.Float(string='Planned Distance (km)', tracking=True)
    fuel_consumed = fields.Float(string='Fuel Consumed (Liters)', tracking=True)
    final_odometer = fields.Float(string='Final Odometer', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('dispatched', 'Dispatched'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', tracking=True)

    def action_dispatch(self):
        for trip in self:
            if trip.state != 'draft':
                raise ValidationError("Only draft trips can be dispatched.")
            if trip.vehicle_id.status != 'available':
                raise ValidationError("Vehicle is not available.")
            if trip.driver_id.status != 'available':
                raise ValidationError("Driver is not available.")
            if trip.driver_id.license_expiry < fields.Date.today():
                raise ValidationError("Driver license has expired.")
            if trip.driver_id.status == 'suspended':
                raise ValidationError("Driver is suspended.")
            if trip.cargo_weight_kg > trip.vehicle_id.max_load_kg:
                raise ValidationError("Cargo weight exceeds vehicle's maximum load capacity.")
            
            trip.vehicle_id.status = 'on_trip'
            trip.driver_id.status = 'on_trip'
            trip.state = 'dispatched'

    def action_complete(self):
        for trip in self:
            if trip.state != 'dispatched':
                raise ValidationError("Only dispatched trips can be completed.")
            
            trip.vehicle_id.status = 'available'
            trip.driver_id.status = 'available'
            trip.state = 'completed'

    def action_cancel(self):
        for trip in self:
            if trip.state == 'dispatched':
                trip.vehicle_id.status = 'available'
                trip.driver_id.status = 'available'
            trip.state = 'cancelled'
