from odoo import models, fields, api
# pyrefly: ignore [missing-import]
from odoo.exceptions import ValidationError

class Maintenance(models.Model):
    _name = 'transitops.maintenance'
    _description = 'Vehicle Maintenance Record'

    vehicle_id = fields.Many2one('transitops.vehicle', string='Vehicle', required=True)
    description = fields.Char(string='Description', required=True)
    cost = fields.Float(string='Cost', required=True)
    active = fields.Boolean(string='Active', default=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.active and record.vehicle_id:
                # Rule 9: New active maintenance record -> vehicle = In Shop
                record.vehicle_id.status = 'in_shop'
        return records

    def action_close(self):
        for record in self:
            record.active = False
            # Rule 10: Close maintenance -> vehicle = Available (unless Retired)
            if record.vehicle_id and record.vehicle_id.status != 'retired':
                record.vehicle_id.status = 'available'

class VehicleInherit(models.Model):
    _inherit = 'transitops.vehicle'

    # Added as per user feedback - simple manual revenue field for demo ROI calculations
    revenue = fields.Float(string='Total Revenue', default=0.0, help='Manual revenue entry for demo/ROI calculations')

    # Computed fields for Dashboard & Reports
    total_maintenance_cost = fields.Float(string='Total Maintenance Cost', compute='_compute_costs')
    total_fuel_cost = fields.Float(string='Total Fuel Cost', compute='_compute_costs')
    total_expense_cost = fields.Float(string='Total Other Expenses', compute='_compute_costs')
    operational_cost = fields.Float(string='Operational Cost', compute='_compute_costs')
    roi_percentage = fields.Float(string='ROI (%)', compute='_compute_costs')

    def _compute_costs(self):
        for vehicle in self:
            m_cost = sum(self.env['transitops.maintenance'].search([('vehicle_id', '=', vehicle.id)]).mapped('cost'))
            f_cost = sum(self.env['transitops.fuel_log'].search([('vehicle_id', '=', vehicle.id)]).mapped('cost'))
            e_cost = sum(self.env['transitops.expense'].search([('vehicle_id', '=', vehicle.id)]).mapped('amount'))
            
            vehicle.total_maintenance_cost = m_cost
            vehicle.total_fuel_cost = f_cost
            vehicle.total_expense_cost = e_cost
            
            op_cost = m_cost + f_cost + e_cost
            vehicle.operational_cost = op_cost

            # ROI = (Revenue - Operational Cost) / Acquisition Cost
            # Note: acquisition_cost exists in base vehicle model per PRD
            # Prevent division by zero
            acq_cost = vehicle.acquisition_cost if hasattr(vehicle, 'acquisition_cost') and vehicle.acquisition_cost else 0
            if acq_cost > 0:
                vehicle.roi_percentage = ((vehicle.revenue - op_cost) / acq_cost) * 100
            else:
                vehicle.roi_percentage = 0.0

