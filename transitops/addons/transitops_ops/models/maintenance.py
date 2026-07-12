from odoo import models, fields, api

class TransitOpsMaintenance(models.Model):
    _name = 'transitops.maintenance'
    _description = 'TransitOps Maintenance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True, tracking=True)
    description = fields.Char(string='Description', required=True)
    cost = fields.Float(string='Cost', required=True, tracking=True)
    active = fields.Boolean(string='Active (In Progress)', default=True, tracking=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(TransitOpsMaintenance, self).create(vals_list)
        for record in records:
            if record.active and record.vehicle_id.status != 'retired':
                record.vehicle_id.status = 'in_shop'
        return records

    def write(self, vals):
        res = super(TransitOpsMaintenance, self).write(vals)
        if 'active' in vals:
            for record in self:
                if record.vehicle_id.status != 'retired':
                    if record.active:
                        record.vehicle_id.status = 'in_shop'
                    else:
                        record.vehicle_id.status = 'available'
        return res

    def action_close(self):
        for record in self:
            record.active = False
