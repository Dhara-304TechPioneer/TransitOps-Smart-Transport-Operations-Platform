{
    "name": "TransitOps Fleet",
    "version": "17.0.1.0.0",
    "category": "Operations",
    "summary": "Driver and Trip Management for TransitOps",
    "depends": [
        "base",
        "transitops_core",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/driver_views.xml",
        "views/trip_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
