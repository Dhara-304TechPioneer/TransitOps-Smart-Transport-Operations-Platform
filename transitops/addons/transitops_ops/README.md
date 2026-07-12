# TransitOps Operations (`transitops_ops`)

This is the **Operations** module for the TransitOps Smart Transport Operations Platform. It manages fleet maintenance, fuel logs, custom expenses (tolls/others), and financial analytics (cost rollups & ROI reporting).

---

## Purpose & Scope

The module manages the backend logic, validation rules, and UI reporting components for vehicle upkeep and financials:

1. **Maintenance State Machine**:
   - **Rule 9**: Creating an active maintenance record automatically transitions the vehicle status to `in_shop` (making it unavailable for cargo trips).
   - **Rule 10**: Closing the maintenance record transitions the vehicle back to `available` (unless it is `retired`).
2. **Fuel and Expense Logs**:
   - Simple entry system for tracking fuel consumption (liters and cost) and operational expenses (like tolls).
3. **Financial Analytics & ROI (Computed Fields)**:
   - Extends the core vehicle model to automatically aggregate and roll up total costs:
     $$\text{Operational Cost} = \text{Total Maintenance Cost} + \text{Total Fuel Cost} + \text{Total Expense Cost}$$
     $$\text{ROI (\%)} = \frac{\text{Total Vehicle Revenue} - \text{Operational Cost}}{\text{Acquisition Cost}} \times 100$$
   - A manual, demo-worthy `revenue` field is added to the vehicle model to facilitate instant ROI metrics showcase.

---

## Data Models Exposed

- `transitops.maintenance`: Fields for vehicle, description, cost, date, and active state.
- `transitops.fuel_log`: Fields for vehicle, liters consumed, cost, and date.
- `transitops.expense`: Categorized (toll/other) expense records.
- `transitops.vehicle` (extended): Addition of `revenue` and computed cost fields.

---

## Directory Structure

```
transitops_ops/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── expense.py
│   ├── fuel_log.py
│   └── maintenance.py          # State machine logic & cost computes
├── security/
│   └── ir.model.access.csv     # Role-based access controls
├── tests/
│   ├── __init__.py
│   └── test_ops.py             # Unit tests suite
└── views/
    ├── fuel_expense_views.xml  # Fuel and Expense Kanban/Tree/Form views
    ├── maintenance_views.xml   # Maintenance Tree/Form/Search views
    └── report_views.xml        # Pivot and Graph reports
```

---

## Integration Dependencies

This module relies on the following modules to compile:
- `transitops_core` (defining security groups and the base `transitops.vehicle` model).
- `transitops_fleet` (defining the base `transitops.driver` and `transitops.trip` models).

Ensure both parent modules are cloned and installed in Odoo before installing `transitops_ops`.

---

## Testing Guidelines

Ensure your virtual environment is active before running commands:
```bash
# Activate python virtual environment from the repo root
.\venv\Scripts\activate
```

### 1. Run Automated Unit Tests
To run the automated tests suite (`tests/test_ops.py`), use the command below from the **repository root**:

```bash
python odoo/odoo-bin -d transitops_db -i transitops_ops --addons-path=odoo/addons,transitops/addons --test-enable --stop-after-init --log-level=test
```

### 2. Update/Install the Module Manually
To check for database schema changes and view imports:

```bash
python odoo/odoo-bin -d transitops_db -u transitops_ops --addons-path=odoo/addons,transitops/addons --stop-after-init
```

### 3. Manual Verification (Demo Script)
To test the business rules in the user interface:
1. Log into Odoo and navigate to the **TransitOps Ops** menu.
2. Select a vehicle and check its status is `available`.
3. Go to **Maintenance** and create a new record for that vehicle. Save it.
4. Go back to the vehicle page: verify its status has automatically changed to `in_shop`.
5. Return to the maintenance record and click **Close Maintenance**.
6. Verify the vehicle status returns to `available`.
7. Add a **Fuel Log** and an **Expense** for the vehicle, then input a manual `revenue` amount on the vehicle's form view.
8. Navigate to **Reports** and verify the pivot tables/graphs reflect the aggregated operational costs and correct ROI calculation.
