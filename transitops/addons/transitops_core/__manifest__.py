{
    'name': 'TransitOps Core',
    'version': '1.0',
    'summary': 'Core module for TransitOps Platform',
    'sequence': 10,
    'description': """
TransitOps Core
===============
This module provides the core functionality and base models for the Smart Transport Operations Platform.
    """,
    'category': 'Operations/TransitOps',
    'website': 'https://www.transitops.example.com',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/vehicle_views.xml',
        'views/dashboard_views.xml',
        'views/login_templates.xml',
        'data/vehicle_status_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'transitops_core/static/src/js/dashboard.js',
            'transitops_core/static/src/xml/dashboard.xml',
            'transitops_core/static/src/css/theme.css',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
