{
    'name': 'TransitOps Fleet',
    'version': '1.1',
    'summary': 'Driver and Trip Management for TransitOps',
    'sequence': 11,
    'description': """
TransitOps Fleet
================
Manages Drivers and Trips, including dispatching logic and business rules.
    """,
    'category': 'Operations/TransitOps',
    'depends': ['transitops_core'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/driver_views.xml',
        'views/vehicle_inherit_views.xml',
        'views/trip_views.xml',
        'reports/trip_report.xml',
        'data/cron_jobs.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
