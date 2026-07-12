from odoo import fields, models


class TransitOpsVehicle(models.Model):
    _name = 'transitops.vehicle'
    _description = 'TransitOps Vehicle'
    _order = 'name'

    name = fields.Char(string='Registration Number', required=True, index=True)
    model_name = fields.Char(string='Model')
    vehicle_type = fields.Selection([
        ('van', 'Van'),
        ('truck', 'Truck'),
        ('bus', 'Bus'),
        ('other', 'Other'),
    ], string='Vehicle Type', default='van', required=True)
    max_load_kg = fields.Float(string='Maximum Load (kg)')
    odometer = fields.Float(string='Odometer (km)')
    acquisition_cost = fields.Float(string='Acquisition Cost')
    status = fields.Selection([
        ('available', 'Available'),
        ('on_trip', 'On Trip'),
        ('in_shop', 'In Shop'),
        ('retired', 'Retired'),
    ], default='available', required=True)

    _sql_constraints = [
        ('registration_number_unique', 'unique(name)', 'Registration number must be unique.'),
    ]
