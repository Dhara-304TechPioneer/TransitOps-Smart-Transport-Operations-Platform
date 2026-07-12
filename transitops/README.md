# 🚍 TransitOps — Smart Transport Operations Platform

> **Odoo 17 Hackathon Project** · 3-Dev Team · Built with Antigravity + Codex

TransitOps is a fleet management and transport operations platform built as a set of custom Odoo 17 modules. It replaces manual spreadsheets and logbooks with a structured, rule-enforced system covering the full lifecycle of a vehicle — from registration and dispatch through maintenance, fuel tracking, and financial analytics.

---

## 📐 Architecture Overview

The project is split into **3 independent Odoo modules**, each owned by a different developer. This separation ensures zero git merge conflicts — each dev commits only within their own addon folder.

```
transitops/addons/
├── transitops_core/        # DEV A — Vehicle Registry, RBAC, Dashboard
├── transitops_fleet/       # DEV B — Driver Management, Trip Dispatch Engine
└── transitops_ops/         # DEV C — Maintenance, Fuel Logs, Expenses, Reports
```

The dependency chain flows one-way:

```
transitops_core  ──▶  transitops_fleet  ──▶  transitops_ops
```

---

## 📦 Modules

### `transitops_core` (Dev A)
Defines the foundation of the platform.

- **Vehicle Registry** — CRUD with unique registration number validation, vehicle type, max load capacity, odometer, and acquisition cost.
- **RBAC** — Defines 4 Odoo security groups: Fleet Manager, Driver, Safety Officer, Financial Analyst.
- **Dashboard** — KPI tiles for active vehicles, in-maintenance vehicles, active trips, pending trips, drivers on duty, and fleet utilization %.

### `transitops_fleet` (Dev B)
Manages people and movement.

- **Driver Management** — Driver profiles with license number, expiry date, category, safety score, and status tracking.
- **Trip Dispatch Engine** — Full state machine: `draft → dispatched → completed / cancelled`.
  - Enforces all 5 mandatory business rules (expired license check, cargo weight limit, vehicle availability, driver availability).
  - Auto-transitions vehicle and driver status on dispatch, completion, and cancellation.

### `transitops_ops` (Dev C) — ✅ Complete
Handles operations, compliance, and financials.

- **Maintenance** — Create maintenance records with auto vehicle status transitions.
- **Fuel Logs** — Log fuel consumption and cost per vehicle.
- **Expenses** — Track toll and other operational expenses.
- **Reports & Analytics** — Pivot tables and bar/pie charts for fuel efficiency and operational cost analysis.
- **ROI Computation** — Computed operational cost and ROI percentage per vehicle.

---

## ✅ Mandatory Business Rules (Judge-Tested)

| # | Rule | Enforced By |
|---|------|-------------|
| 1 | Vehicle registration number is unique | `transitops_core` (SQL constraint) |
| 2 | Retired/In-Shop vehicles excluded from dispatch | `transitops_fleet` (domain filter + server validation) |
| 3 | Expired-license or Suspended drivers excluded | `transitops_fleet` (domain filter + server validation) |
| 4 | On-Trip vehicle/driver cannot be reassigned | `transitops_fleet` (model validation) |
| 5 | Cargo weight ≤ vehicle max load capacity | `transitops_fleet` (`action_dispatch`) |
| 6 | Dispatch → vehicle + driver status = `on_trip` | `transitops_fleet` (`action_dispatch`) |
| 7 | Complete → both status = `available` | `transitops_fleet` (`action_complete`) |
| 8 | Cancel from Dispatched → both = `available` | `transitops_fleet` (`action_cancel`) |
| 9 | New active maintenance → vehicle = `in_shop` | **`transitops_ops`** (`Maintenance.create`) |
| 10 | Close maintenance → vehicle = `available` (unless Retired) | **`transitops_ops`** (`Maintenance.action_close`) |

---

## 🗺️ Data Models

```
transitops.vehicle       name, model_name, vehicle_type, max_load_kg, odometer,
                         acquisition_cost, revenue*, status

transitops.driver        name, license_number, license_category, license_expiry,
                         contact_number, safety_score, status

transitops.trip          source, destination, vehicle_id, driver_id,
                         cargo_weight_kg, planned_distance_km,
                         fuel_consumed, final_odometer, state

transitops.maintenance   vehicle_id, description, cost, active, date

transitops.fuel_log      vehicle_id, liters, cost, date

transitops.expense       vehicle_id, category (toll/other), amount, date
```
> `*` `revenue` is a manual demo field added by `transitops_ops` for ROI calculations.

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.11
- PostgreSQL 15
- Odoo 17 Community (located in the `odoo/` subdirectory of this repo)

### 1. Clone the repo and activate the virtual environment
```bash
git clone <repo-url>
cd TransitOps-Smart-Transport-Operations-Platform
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # macOS/Linux
```

### 2. Create the database and install all modules
```bash
python odoo/odoo-bin \
  -d transitops_db \
  -i transitops_core,transitops_fleet,transitops_ops \
  --addons-path=odoo/addons,transitops/addons \
  --stop-after-init
```

### 3. Start the Odoo server
```bash
python odoo/odoo-bin \
  -d transitops_db \
  --addons-path=odoo/addons,transitops/addons
```
Open your browser at **http://localhost:8069**.

---

## 🧪 Testing

### Run the full test suite
```bash
python odoo/odoo-bin \
  -d transitops_db \
  -i transitops_ops \
  --addons-path=odoo/addons,transitops/addons \
  --test-enable \
  --stop-after-init \
  --log-level=test
```

### Run tests for a specific module
```bash
# transitops_ops only
python odoo/odoo-bin \
  -d transitops_db \
  -u transitops_ops \
  --addons-path=odoo/addons,transitops/addons \
  --test-enable \
  --stop-after-init \
  --log-level=test
```

### What the tests cover (`transitops_ops/tests/test_ops.py`)

| Test | What it validates |
|------|------------------|
| `test_01_maintenance_state_transitions` | Rule #9 (vehicle → `in_shop`) and Rule #10 (vehicle → `available`) |
| `test_02_maintenance_on_retired_vehicle` | Closing maintenance on a retired vehicle keeps it `retired` |
| `test_03_cost_and_roi_calculations` | Correct aggregation of maintenance, fuel, and expense costs; ROI formula |

---

## 🎬 Demo Script (Acceptance Test from PRD §1.6)

This is the exact scenario judges will walk through:

1. **Register Van-05** (500 kg max load, set `acquisition_cost` and `revenue` for ROI demo).
2. **Register Driver Alex** with a valid license and `available` status.
3. **Create a Trip** — source, destination, cargo weight = 450 kg, assign Van-05 and Alex.
4. **Dispatch** the trip → both Van-05 and Alex flip to `on_trip`.
5. **Complete** the trip → both return to `available`.
6. **Create a Maintenance Record** for Van-05 → Van-05 status instantly changes to `in_shop` (hidden from new trip dispatch).
7. **Close Maintenance** → Van-05 returns to `available`.
8. **Log Fuel and Expense** records for Van-05.
9. **Open Reports** → Verify pivot tables show the correct operational cost and ROI.

---

## 👥 Team Ownership Map

| Developer | Module | Owns |
|-----------|--------|------|
| Dev A | `transitops_core` | Vehicle model, RBAC groups, Dashboard |
| Dev B | `transitops_fleet` | Driver, Trip, Dispatch state machine |
| Dev C | `transitops_ops` | Maintenance, Fuel, Expense, Reports |

> **Golden Rule**: Each developer commits **only** inside their own `addons/transitops_X/` folder. Cross-module references go through Odoo's `depends` system — never direct file imports.

---

## 📂 Full Directory Reference

```
TransitOps-Smart-Transport-Operations-Platform/
├── odoo/                           # Odoo 17 Community source
├── transitops/
│   ├── README.md                   # ← You are here
│   ├── addons/
│   │   ├── transitops_core/        # Dev A
│   │   ├── transitops_fleet/       # Dev B
│   │   └── transitops_ops/         # Dev C (complete)
│   └── docs/
│       └── TransitOps_PRD_TRD_DesignStack.md
└── venv/
```
