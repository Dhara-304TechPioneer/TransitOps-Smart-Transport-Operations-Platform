{
    'name': 'TransitOps Operations',
    'version': '1.1',
    'summary': 'Maintenance, Fuel, Expenses and Reports',
    'sequence': 12,
    'description': """
TransitOps Operations
=====================
Handles operations, compliance, financials, and ROI computations.
    """,
    'category': 'Operations/TransitOps',
    'depends': ['transitops_fleet'],
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_views.xml',
        'views/fuel_expense_views.xml',
        'views/vehicle_inherit_views.xml',
        'views/report_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
