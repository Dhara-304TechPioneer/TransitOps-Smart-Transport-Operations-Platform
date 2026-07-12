from odoo import api, fields, models, _
from odoo.exceptions import UserError


class TransitOpsMaintenance(models.Model):
    _name = 'transitops.maintenance'
    _description = 'TransitOps Maintenance'
    _order = 'date desc, id desc'

    vehicle_id = fields.Many2one('transitops.vehicle', required=True, ondelete='restrict')
    description = fields.Char(required=True)
    cost = fields.Monetary(required=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    active = fields.Boolean(default=True, help='Uncheck to close this maintenance record.')
    date = fields.Date(default=fields.Date.today, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records.filtered('active'):
            if record.vehicle_id.status == 'on_trip':
                raise UserError(_('A vehicle on a trip cannot enter maintenance.'))
            if record.vehicle_id.status != 'retired':
                record.vehicle_id.status = 'in_shop'
        return records

    def write(self, vals):
        result = super().write(vals)
        if 'active' in vals:
            for record in self:
                if record.active:
                    if record.vehicle_id.status == 'on_trip':
                        raise UserError(_('A vehicle on a trip cannot enter maintenance.'))
                    if record.vehicle_id.status != 'retired':
                        record.vehicle_id.status = 'in_shop'
                elif record.vehicle_id.status != 'retired':
                    other_open = self.search_count([('vehicle_id', '=', record.vehicle_id.id), ('active', '=', True)])
                    if not other_open:
                        record.vehicle_id.status = 'available'
        return result

    def action_close(self):
        self.write({'active': False})
        return True
