{
    'name': 'TransitOps Core',
    'version': '17.0.1.0.0',
    'summary': 'Fleet vehicle registry and operations dashboard',
    'category': 'Operations',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/vehicle_status_data.xml',
        'views/vehicle_views.xml',
        'views/dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': ['transitops_core/static/src/js/dashboard.js'],
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
