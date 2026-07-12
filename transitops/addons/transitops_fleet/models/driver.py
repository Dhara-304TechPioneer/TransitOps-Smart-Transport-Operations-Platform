from odoo import models, fields

class TransitOpsDriver(models.Model):
    _name = 'transitops.driver'
    _description = 'TransitOps Driver'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    license_number = fields.Char(string='License Number', required=True, tracking=True)
    license_category = fields.Char(string='License Category', tracking=True)
    license_expiry = fields.Date(string='License Expiry', required=True, tracking=True)
    contact_number = fields.Char(string='Contact Number', tracking=True)
    safety_score = fields.Float(string='Safety Score', tracking=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('on_trip', 'On Trip'),
        ('off_duty', 'Off Duty'),
        ('suspended', 'Suspended'),
    ], string='Status', default='available', tracking=True)
