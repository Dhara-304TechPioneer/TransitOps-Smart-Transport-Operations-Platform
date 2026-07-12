# TransitOps — PRD + TRD + Design Stack
Odoo Hackathon · 3-dev team · 4hr MVP window · Tools: Antigravity + Codex

---

## 0. Strategy for 4hr win (read first)

4hr = no time for full 8hr scope. Cut ruthlessly. MVP = only what judges score highest:
working auth+RBAC, vehicle/driver CRUD, trip lifecycle with validations, auto status
transitions, one dashboard. Maintenance + fuel/expense simplified. Bonus features (PDF
export, email reminders, dark mode) → skip unless time left.

**Split by module ownership, not by layer.** Each dev owns full vertical slice (model +
view + logic) for their domain. This avoids merge conflicts since Odoo modules live in
separate addon folders — git conflicts near-zero if folder boundaries respected.

| Dev | Owns | Odoo module |
|---|---|---|
| Dev A | Auth/RBAC, Vehicle Registry, Dashboard shell | `transitops_core` |
| Dev B | Driver Management, Trip Management (dispatch engine) | `transitops_fleet` |
| Dev C | Maintenance, Fuel & Expense, Reports/Analytics | `transitops_ops` |

Rule: **nobody edits another dev's module folder.** Cross-module refs go through
Odoo's own dependency system (`depends` in `__manifest__.py`), not shared files.

---

## 1. PRD — Product Requirements Document

### 1.1 Problem
Manual spreadsheets/logbooks for fleet ops → scheduling conflicts, missed maintenance,
expired licenses, no expense visibility.

### 1.2 Users & goals (from brief)
- **Fleet Manager** — fleet health, vehicle lifecycle, maintenance oversight.
- **Driver** — create/monitor own trips.
- **Safety Officer** — license validity, driver compliance/safety score.
- **Financial Analyst** — cost, fuel, ROI visibility.

### 1.3 MVP scope (must-ship in 4hr)
1. Login + RBAC (4 roles above map to Odoo security groups).
2. Vehicle Registry: CRUD, unique reg number, status enum.
3. Driver Management: CRUD, license expiry field, status enum.
4. Trip Management: create → dispatch → complete/cancel, with all 5 mandatory
   validation rules enforced server-side.
5. Maintenance: create record → auto flips vehicle to In Shop; close → restores.
6. Dashboard: KPI tiles (Active/Available/In Maintenance vehicles, Active/Pending
   trips, Drivers On Duty, Fleet Utilization %).
7. Fuel log (liters, cost, date) linked to vehicle; simple cost rollup.

### 1.4 Explicitly OUT of MVP (do only if time remains)
- PDF export, email reminders, dark mode, advanced charts, CSV export polish,
  vehicle document uploads, multi-region filters.

### 1.5 Mandatory business rules (non-negotiable, judge will test these)
1. Vehicle registration number unique.
2. Retired/In Shop vehicles excluded from dispatch dropdown.
3. Expired-license or Suspended drivers excluded from dispatch dropdown.
4. On Trip vehicle/driver cannot be assigned again.
5. Cargo weight ≤ vehicle max load capacity.
6. Dispatch → vehicle+driver status = On Trip.
7. Complete → both back to Available.
8. Cancel (from Dispatched) → both back to Available.
9. New active maintenance record → vehicle = In Shop.
10. Close maintenance → vehicle = Available (unless Retired).

### 1.6 Acceptance test (from brief §5) — use as demo script
Register Van-05 (500kg) → register driver Alex → trip cargo 450kg → dispatch (pass,
both On Trip) → complete trip (both Available) → create maintenance (vehicle In
Shop, hidden from dispatch) → dashboard/report reflects updated cost.

---

## 2. TRD — Technical Requirements Document

### 2.1 Stack
- **Framework:** Odoo 17 (Community), Python 3.11, PostgreSQL 15.
- **Backend:** Odoo ORM (`models.Model`), server actions for state machine logic.
- **Frontend:** Odoo native views (list/form/kanban) + OWL component only for
  Dashboard KPI widget (custom JS minimal, time-boxed).
- **Auth:** Odoo native `res.users` + `res.groups` (RBAC), no external auth — fastest
  path, judge doesn't need custom login UI.
- **Dev tooling:** Antigravity/Codex for scaffolding models/views/XML fast; each dev
  runs local Odoo instance pointed at own DB during dev, merge to shared DB only at
  integration checkpoints (hour 2 and hour 3.5).

### 2.2 Data model (Odoo model names)

```
transitops.vehicle
  name (Char, "Registration Number", unique constraint)
  model_name (Char)
  vehicle_type (Selection)
  max_load_kg (Float)
  odometer (Float)
  acquisition_cost (Float)
  status (Selection: available/on_trip/in_shop/retired) default=available

transitops.driver
  name (Char)
  license_number (Char)
  license_category (Char)
  license_expiry (Date)
  contact_number (Char)
  safety_score (Float)
  status (Selection: available/on_trip/off_duty/suspended) default=available

transitops.trip
  source (Char)
  destination (Char)
  vehicle_id (Many2one transitops.vehicle)
  driver_id (Many2one transitops.driver)
  cargo_weight_kg (Float)
  planned_distance_km (Float)
  fuel_consumed (Float)      # filled on complete
  final_odometer (Float)     # filled on complete
  state (Selection: draft/dispatched/completed/cancelled) default=draft

transitops.maintenance
  vehicle_id (Many2one transitops.vehicle)
  description (Char)
  cost (Float)
  active (Boolean) default=True   # False = closed
  date (Date)

transitops.fuel_log
  vehicle_id (Many2one transitops.vehicle)
  liters (Float)
  cost (Float)
  date (Date)

transitops.expense
  vehicle_id (Many2one transitops.vehicle)
  category (Selection: toll/other)
  amount (Float)
  date (Date)
```

### 2.3 State machine / business logic placement
Put ALL rule-enforcement in model methods (`write`, `action_dispatch`,
`action_complete`, `action_cancel`), never in view/JS. Judges + future maintainers
read model code as source of truth.

```python
# transitops.trip (pseudocode, exact rule mapping to PRD 1.5)
def action_dispatch(self):
    for trip in self:
        if trip.vehicle_id.status != 'available':
            raise ValidationError("Vehicle not available")
        if trip.driver_id.status != 'available':
            raise ValidationError("Driver not available")
        if trip.driver_id.license_expiry < fields.Date.today():
            raise ValidationError("Driver license expired")
        if trip.driver_id.status == 'suspended':
            raise ValidationError("Driver suspended")
        if trip.cargo_weight_kg > trip.vehicle_id.max_load_kg:
            raise ValidationError("Cargo exceeds capacity")
        trip.vehicle_id.status = 'on_trip'
        trip.driver_id.status = 'on_trip'
        trip.state = 'dispatched'

def action_complete(self):
    for trip in self:
        trip.vehicle_id.status = 'available'
        trip.driver_id.status = 'available'
        trip.state = 'completed'

def action_cancel(self):
    for trip in self:
        if trip.state == 'dispatched':
            trip.vehicle_id.status = 'available'
            trip.driver_id.status = 'available'
        trip.state = 'cancelled'
```

Dispatch pool filters (domain on `vehicle_id`/`driver_id` fields in trip form view):
`[('status','=','available')]` — this alone satisfies rules 2+3+4 at UI level;
model-level checks above are the real enforcement (defense in depth, and judges may
test via API/shell not just UI).

### 2.4 RBAC groups (`security/security.xml`)
`transitops.group_fleet_manager`, `group_driver`, `group_safety_officer`,
`group_financial_analyst`. Record rules scoped per model — e.g. Financial Analyst
read-only on vehicle/driver, full on expense/fuel/reports.

### 2.5 Dashboard KPIs (computed, not stored)
Server action / controller returning JSON consumed by OWL widget:
active_vehicles, available_vehicles, in_maintenance, active_trips, pending_trips,
drivers_on_duty, fleet_utilization = active_trips / total_vehicles * 100.

### 2.6 Reports formulas (brief §3.8)
- Fuel Efficiency = planned_distance_km / fuel_consumed (per trip, aggregate per vehicle)
- Operational Cost (per vehicle) = SUM(fuel_log.cost) + SUM(maintenance.cost)
- Vehicle ROI = (Revenue − (Maintenance + Fuel)) / Acquisition Cost
  — Revenue field not in original entity list; add `revenue` Float on trip or vehicle
  (assumption, flag to team: brief doesn't define revenue source — decide now, don't
  block on it later).

---

## 3. Design / UI reference
Excalidraw mockup screenshot shows dark theme, left sidebar nav, top KPI card row,
data tables with colored status pill badges (green/orange/yellow/blue), and a
bar-chart panel bottom-right. Replicate via Odoo's built-in dark-mode-capable
backend theme + custom status-badge widget (small CSS, ~30 min task, assign to
whoever finishes their module first — not core-path, don't block on it).

---

## 4. Modular Directory Structure (SOLID + zero merge-conflict)

```
transitops/                          # repo root
├── addons/
│   ├── transitops_core/             # DEV A — owns entirely
│   │   ├── __init__.py
│   │   ├── __manifest__.py          # depends: ['base','mail']
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── vehicle.py
│   │   ├── views/
│   │   │   ├── vehicle_views.xml
│   │   │   └── dashboard_views.xml
│   │   ├── security/
│   │   │   ├── security.xml         # role groups defined HERE only
│   │   │   └── ir.model.access.csv
│   │   ├── static/src/js/dashboard.js
│   │   └── data/vehicle_status_data.xml
│   │
│   ├── transitops_fleet/            # DEV B — owns entirely
│   │   ├── __init__.py
│   │   ├── __manifest__.py          # depends: ['transitops_core']
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── driver.py
│   │   │   └── trip.py
│   │   ├── views/
│   │   │   ├── driver_views.xml
│   │   │   └── trip_views.xml
│   │   └── security/ir.model.access.csv
│   │
│   └── transitops_ops/              # DEV C — owns entirely
│       ├── __init__.py
│       ├── __manifest__.py          # depends: ['transitops_fleet']
│       ├── models/
│       │   ├── __init__.py
│       │   ├── maintenance.py
│       │   ├── fuel_log.py
│       │   └── expense.py
│       ├── views/
│       │   ├── maintenance_views.xml
│       │   ├── fuel_expense_views.xml
│       │   └── report_views.xml
│       └── security/ir.model.access.csv
│
├── docs/
│   └── TransitOps_PRD_TRD_DesignStack.md   # this file
└── README.md                        # setup + demo script
```

### SOLID mapping (why this avoids conflicts)
- **S**ingle Responsibility → 1 module = 1 domain, 1 owner, 1 file set.
- **O**pen/Closed → `transitops_fleet`/`_ops` *extend* core via `depends`, never edit
  core files directly (e.g. adding a field to vehicle from fleet module uses
  inheritance: `_inherit = 'transitops.vehicle'` in a file inside `_fleet`, not by
  touching core's `vehicle.py`).
- **L**iskov / **I**nterface seg → each model exposes clean action methods
  (`action_dispatch`, `action_complete`) other modules call, not raw field writes.
- **D**ependency inversion → cross-module data access via `env['model.name']`
  lookups declared in manifest `depends`, never file imports across addon folders.

**Golden rule for zero git conflicts:** each dev commits only inside their own
`addons/transitops_X/` folder. `__manifest__.py` files never edited by anyone but
owner. If Dev B needs a core field, ask Dev A to add it — don't touch core files.

---

## 5. 4-hour execution timeline

| Time | Milestone |
|---|---|
| 0:00–0:20 | Repo scaffold, 3 empty modules boot in Odoo, manifests + security stub. All 3 confirm local Odoo runs. |
| 0:20–2:00 | Parallel build: models + basic views per owner. |
| 2:00–2:20 | **Checkpoint 1**: merge, install all 3 modules together, fix boot errors. |
| 2:20–3:30 | Parallel: business rules, dashboard KPIs, trip state machine, maintenance auto-status. |
| 3:30–3:50 | **Checkpoint 2**: full merge, run acceptance test script (§1.6). |
| 3:50–4:00 | Demo rehearsal, seed data, buffer. |

---

## 6. Open assumptions to confirm with team now
- ROI "Revenue" field source undefined in brief — need decision (add manual field vs skip ROI).
- CSV export: use Odoo's built-in list-view export (free, no code) — satisfies req without custom work.
- Auth: using Odoo native login, not custom email/password screen — faster, still meets "secure login" requirement.
