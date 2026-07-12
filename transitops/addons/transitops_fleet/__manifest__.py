{
    'name': 'TransitOps Fleet',
    'version': '1.0',
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
        'views/driver_views.xml',
        'views/trip_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
