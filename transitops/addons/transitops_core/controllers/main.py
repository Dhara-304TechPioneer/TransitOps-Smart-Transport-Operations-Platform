import json
from odoo import http
from odoo.http import request

class TransitOpsDashboard(http.Controller):
    @http.route('/transitops/dashboard_data', type='json', auth='user')
    def get_dashboard_data(self):
        # We need to make sure the fleet and ops modules are installed before querying their models
        # If not, we will just return 0 for those stats.
        
        vehicle_env = request.env['transitops.vehicle']
        
        active_vehicles = vehicle_env.search_count([('active', '=', True)])
        available_vehicles = vehicle_env.search_count([('status', '=', 'available')])
        in_maintenance = vehicle_env.search_count([('status', '=', 'in_shop')])
        
        # Check if trip model exists (transitops_fleet might not be installed)
        active_trips = 0
        pending_trips = 0
        if 'transitops.trip' in request.env:
            trip_env = request.env['transitops.trip']
            active_trips = trip_env.search_count([('state', '=', 'dispatched')])
            pending_trips = trip_env.search_count([('state', '=', 'draft')])

        # Check if driver model exists
        drivers_on_duty = 0
        if 'transitops.driver' in request.env:
            drivers_on_duty = request.env['transitops.driver'].search_count([('status', '=', 'on_trip')])

        fleet_utilization = 0.0
        if active_vehicles > 0:
            fleet_utilization = (active_trips / active_vehicles) * 100

        # Fetch Recent Vehicles
        recent_vehicles = []
        for v in vehicle_env.search([], order='id desc', limit=5):
            recent_vehicles.append({
                'name': v.name,
                'model_name': v.model_name or 'N/A',
                'status': v.status
            })

        # Fetch Recent Trips and Chart Data
        recent_trips = []
        trip_counts = {'draft': 0, 'dispatched': 0, 'completed': 0, 'cancelled': 0}
        
        if 'transitops.trip' in request.env:
            trip_env = request.env['transitops.trip']
            for t in trip_env.search([], order='id desc', limit=5):
                recent_trips.append({
                    'source': t.source,
                    'destination': t.destination,
                    'vehicle': t.vehicle_id.name if t.vehicle_id else 'N/A',
                    'driver': t.driver_id.name if t.driver_id else 'N/A',
                    'state': t.state
                })
            # Chart breakdown
            trip_counts['draft'] = trip_env.search_count([('state', '=', 'draft')])
            trip_counts['dispatched'] = trip_env.search_count([('state', '=', 'dispatched')])
            trip_counts['completed'] = trip_env.search_count([('state', '=', 'completed')])
            trip_counts['cancelled'] = trip_env.search_count([('state', '=', 'cancelled')])

        return {
            'active_vehicles': active_vehicles,
            'available_vehicles': available_vehicles,
            'in_maintenance': in_maintenance,
            'active_trips': active_trips,
            'pending_trips': pending_trips,
            'drivers_on_duty': drivers_on_duty,
            'fleet_utilization': round(fleet_utilization, 2),
            'recent_vehicles': recent_vehicles,
            'recent_trips': recent_trips,
            'chart_data': [
                trip_counts['draft'], 
                trip_counts['dispatched'], 
                trip_counts['completed'], 
                trip_counts['cancelled']
            ]
        }
