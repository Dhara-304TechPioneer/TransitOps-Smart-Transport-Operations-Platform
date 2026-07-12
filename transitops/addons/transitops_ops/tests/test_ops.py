# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestTransitOps(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestTransitOps, cls).setUpClass()
        # We need to create a test vehicle.
        # Since transitops_ops depends on transitops_core, transitops.vehicle should exist.
        cls.vehicle = cls.env['transitops.vehicle'].create({
            'name': 'TEST-VAN-01',
            'model_name': 'Test Cargo Van',
            'vehicle_type': 'van',
            'max_load_kg': 500.0,
            'odometer': 1000.0,
            'acquisition_cost': 20000.0,
            'status': 'available',
            'revenue': 1000.0,
        })

    def test_01_maintenance_state_transitions(self):
        """Test that vehicle status changes when maintenance is created and closed"""
        # Ensure vehicle starts as available
        self.assertEqual(self.vehicle.status, 'available')

        # 1. Create active maintenance record
        maintenance = self.env['transitops.maintenance'].create({
            'vehicle_id': self.vehicle.id,
            'description': 'Engine Oil Change',
            'cost': 150.0,
            'active': True,
        })

        # Rule 9 Check: Status should flip to 'in_shop'
        self.assertEqual(self.vehicle.status, 'in_shop')

        # 2. Close the maintenance record
        maintenance.action_close()

        # Rule 10 Check: Status should restore to 'available'
        self.assertFalse(maintenance.active)
        self.assertEqual(self.vehicle.status, 'available')

    def test_02_maintenance_on_retired_vehicle(self):
        """Test that closing maintenance on a retired vehicle keeps it retired"""
        self.vehicle.status = 'retired'

        maintenance = self.env['transitops.maintenance'].create({
            'vehicle_id': self.vehicle.id,
            'description': 'Final Inspection',
            'cost': 50.0,
            'active': True,
        })

        # Closing should keep it retired
        maintenance.action_close()
        self.assertEqual(self.vehicle.status, 'retired')

    def test_03_cost_and_roi_calculations(self):
        """Test computed costs rollups and ROI calculation on the vehicle"""
        # Create Maintenance
        self.env['transitops.maintenance'].create({
            'vehicle_id': self.vehicle.id,
            'description': 'Tire rotation',
            'cost': 200.0,
        })

        # Create Fuel Log
        self.env['transitops.fuel_log'].create({
            'vehicle_id': self.vehicle.id,
            'liters': 40.0,
            'cost': 80.0,
        })

        # Create Expense
        self.env['transitops.expense'].create({
            'vehicle_id': self.vehicle.id,
            'category': 'toll',
            'amount': 20.0,
        })

        # Force recomputation of cost fields
        self.vehicle._compute_costs()

        # Check total costs
        self.assertEqual(self.vehicle.total_maintenance_cost, 200.0)
        self.assertEqual(self.vehicle.total_fuel_cost, 80.0)
        self.assertEqual(self.vehicle.total_expense_cost, 20.0)
        
        # Operational Cost = Maintenance + Fuel + Expense = 200 + 80 + 20 = 300
        self.assertEqual(self.vehicle.operational_cost, 300.0)

        # ROI = (Revenue - Operational Cost) / Acquisition Cost = (1000 - 300) / 20000 = 700 / 20000 = 0.035 = 3.5%
        self.assertEqual(self.vehicle.roi_percentage, 3.5)
