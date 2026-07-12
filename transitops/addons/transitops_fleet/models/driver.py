from odoo import fields, models


class TransitOpsDriver(models.Model):
    _name = 'transitops.driver'
    _description = 'TransitOps Driver'
    _order = 'name'

    name = fields.Char(required=True)
    license_number = fields.Char(required=True, index=True)
    license_category = fields.Char()
    license_expiry = fields.Date(required=True)
    contact_number = fields.Char()
    safety_score = fields.Float(default=100.0)
    status = fields.Selection([('available', 'Available'), ('on_trip', 'On Trip'), ('off_duty', 'Off Duty'), ('suspended', 'Suspended')], default='available', required=True)

    _sql_constraints = [('license_number_unique', 'unique(license_number)', 'License number must be unique.')]
