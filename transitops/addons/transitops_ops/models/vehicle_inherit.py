from odoo import models, fields, api

class TransitOpsVehicleInherit(models.Model):
    _inherit = 'transitops.vehicle'

    maintenance_ids = fields.One2many('transitops.maintenance', 'vehicle_id', string='Maintenance Records')
    fuel_log_ids = fields.One2many('transitops.fuel_log', 'vehicle_id', string='Fuel Logs')

    total_maintenance_cost = fields.Float(string='Total Maintenance Cost', compute='_compute_financials', store=True)
    total_fuel_cost = fields.Float(string='Total Fuel Cost', compute='_compute_financials', store=True)
    operational_cost = fields.Float(string='Operational Cost', compute='_compute_financials', store=True)
    roi_percentage = fields.Float(string='ROI (%)', compute='_compute_financials', store=True)

    @api.depends('maintenance_ids.cost', 'fuel_log_ids.cost', 'acquisition_cost', 'revenue')
    def _compute_financials(self):
        for vehicle in self:
            vehicle.total_maintenance_cost = sum(vehicle.maintenance_ids.mapped('cost'))
            vehicle.total_fuel_cost = sum(vehicle.fuel_log_ids.mapped('cost'))
            vehicle.operational_cost = vehicle.total_maintenance_cost + vehicle.total_fuel_cost
            
            if vehicle.acquisition_cost and vehicle.acquisition_cost > 0:
                vehicle.roi_percentage = ((vehicle.revenue - vehicle.operational_cost) / vehicle.acquisition_cost) * 100
            else:
                vehicle.roi_percentage = 0.0
