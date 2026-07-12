from odoo import api, fields, models, _

class TransitOpsVehicle(models.Model):
    _name = 'transitops.vehicle'
    _description = 'TransitOps Vehicle'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Registration Number', required=True, copy=False, index=True)
    model_name = fields.Char(string='Model Name', tracking=True)
    vehicle_type = fields.Selection([
        ('car', 'Car'),
        ('van', 'Van'),
        ('truck', 'Truck'),
        ('bus', 'Bus'),
    ], string='Vehicle Type', tracking=True)
    max_load_kg = fields.Float(string='Max Load (kg)', tracking=True)
    odometer = fields.Float(string='Odometer (km)', tracking=True)
    acquisition_cost = fields.Float(string='Acquisition Cost', tracking=True)
    revenue = fields.Float(string='Revenue', tracking=True, help="Used for ROI calculations")
    status = fields.Selection([
        ('available', 'Available'),
        ('on_trip', 'On Trip'),
        ('in_shop', 'In Shop'),
        ('retired', 'Retired'),
    ], string='Status', default='available', tracking=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Vehicle registration number must be unique!')
    ]
