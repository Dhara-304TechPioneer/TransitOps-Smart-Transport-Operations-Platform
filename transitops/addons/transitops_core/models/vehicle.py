from odoo import fields, models

class TransitOpsVehicle(models.Model):
    _name = "transitops.vehicle"
    _description = "TransitOps Vehicle"

    name = fields.Char(string="Registration Number", required=True)
    model_name = fields.Char(string="Model Name")
    vehicle_type = fields.Selection(
        selection=[
            ("truck", "Truck"),
            ("van", "Van"),
            ("car", "Car"),
        ],
        string="Vehicle Type",
    )
    max_load_kg = fields.Float(string="Max Load (kg)")
    odometer = fields.Float(string="Odometer")
    acquisition_cost = fields.Float(string="Acquisition Cost")
    status = fields.Selection(
        selection=[
            ("available", "Available"),
            ("on_trip", "On Trip"),
            ("in_shop", "In Shop"),
            ("retired", "Retired"),
        ],
        string="Status",
        default="available",
    )

    _sql_constraints = [
        ("name_uniq", "unique(name)", "The vehicle registration number must be unique!"),
    ]
