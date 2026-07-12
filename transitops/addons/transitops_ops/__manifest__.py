{
    'name': 'TransitOps Operations',
    'version': '1.0',
    'summary': 'Maintenance, Fuel Logs, and Expense management for TransitOps',
    'description': 'Handles fleet maintenance, fuel logging, and expense tracking for the TransitOps system.',
    'category': 'Operations',
    'author': 'Hackathon Team - Dev C',
    'depends': ['transitops_fleet'], # TRD: transitops_ops depends on transitops_fleet (which depends on core)
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_views.xml',
        'views/fuel_expense_views.xml',
        'views/report_views.xml',
    ],
    'installable': True,
    'application': False,
}
