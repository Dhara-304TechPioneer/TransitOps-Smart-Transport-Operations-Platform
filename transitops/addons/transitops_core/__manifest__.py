{
    'name': 'TransitOps Core',
    'version': '17.0.1.0.0',
    'summary': 'Core module for TransitOps',
    'description': 'Core models and base configuration for the TransitOps Smart Transport Operations Platform.',
    'category': 'Operations',
    'author': 'Hackathon Team',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
}