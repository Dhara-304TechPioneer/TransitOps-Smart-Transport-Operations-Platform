from odoo import models, fields, api

class TransitOpsDriver(models.Model):
    _name = 'transitops.driver'
    _description = 'TransitOps Driver'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Driver Name', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Related User', help="The Odoo user account for this driver")
    license_number = fields.Char(string='License Number', required=True, tracking=True)
    license_category = fields.Char(string='License Category', tracking=True)
    license_expiry = fields.Date(string='License Expiry', required=True, tracking=True)
    contact_number = fields.Char(string='Contact Number', tracking=True)
    safety_score = fields.Integer(string='Safety Score (0-100)', default=100, tracking=True)
    active = fields.Boolean(default=True)
    trip_count = fields.Integer(string='Trip Count', compute='_compute_trip_count')

    def _compute_trip_count(self):
        for driver in self:
            driver.trip_count = self.env['transitops.trip'].search_count([('driver_id', '=', driver.id)])

    status = fields.Selection([
        ('available', 'Available'),
        ('on_trip', 'On Trip'),
        ('off_duty', 'Off Duty'),
        ('suspended', 'Suspended'),
    ], string='Status', default='available', tracking=True)

    region = fields.Selection([
        ('north', 'North Region'),
        ('south', 'South Region'),
        ('east', 'East Region'),
        ('west', 'West Region')
    ], string='Region', tracking=True)

    @api.model
    def _cron_check_license_expiry(self):
        # Find drivers with license expiring in next 30 days
        expiry_date = fields.Date.today() + fields.Date.relativedelta(days=30)
        expiring_drivers = self.search([('license_expiry', '<=', expiry_date), ('status', '!=', 'suspended')])
        for driver in expiring_drivers:
            # Post message in chatter to alert followers (Fleet Managers)
            driver.message_post(
                body="Warning: Driver license is expiring on %s!" % driver.license_expiry,
                subject="License Expiry Warning"
            )
