from odoo import fields, models


class TransitOpsDriver(models.Model):
    _name = "transitops.driver"
    _description = "TransitOps Driver"

    name = fields.Char(required=True)
    license_number = fields.Char(required=True)
    license_category = fields.Char()
    license_expiry = fields.Date()
    contact_number = fields.Char()
    safety_score = fields.Float(default=100)
    status = fields.Selection(
        selection=[
            ("available", "Available"),
            ("on_trip", "On Trip"),
            ("off_duty", "Off Duty"),
            ("suspended", "Suspended"),
        ],
        default="available",
    )
