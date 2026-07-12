from odoo import api, fields, models, _

class TransitOpsVehicle(models.Model):
    _name = 'transitops.vehicle'
    _description = 'TransitOps Vehicle'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Registration Number', required=True, copy=False, index=True)
    image_1920 = fields.Image(string="Vehicle Image", max_width=1920, max_height=1920)
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

    # Document Uploads
    registration_document = fields.Binary(string='Registration Document', attachment=True)
    registration_filename = fields.Char(string='Registration Filename')
    insurance_document = fields.Binary(string='Insurance Document', attachment=True)
    insurance_filename = fields.Char(string='Insurance Filename')

    # Multi-Region Support
    region = fields.Selection([
        ('north', 'North Region'),
        ('south', 'South Region'),
        ('east', 'East Region'),
        ('west', 'West Region')
    ], string='Region', tracking=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Vehicle registration number must be unique!')
    ]
