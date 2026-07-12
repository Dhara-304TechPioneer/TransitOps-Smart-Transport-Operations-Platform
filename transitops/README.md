# TransitOps — Smart Transport Operations Platform

Odoo 17 MVP for fleet dispatch, compliance, maintenance, and cost tracking.

## Install

Start Odoo with the custom addons path, then install these modules in order:

```powershell
..\venv\Scripts\python.exe ..\odoo\odoo-bin -d transitops_demo --addons-path=..\odoo\addons,.\addons -i transitops_ops
```

Installing `transitops_ops` installs its `transitops_fleet` and `transitops_core` dependencies.

## Demo flow

1. Give your user the **Fleet Manager** group in TransitOps.
2. Create `VAN-05`, max load `500 kg`, and driver Alex with a future license expiry.
3. Create a `450 kg` draft trip, dispatch it, then complete it.
4. Create a maintenance record for VAN-05; its status becomes **In Shop**. Close the record to restore **Available**.
5. Add a fuel log and inspect **Cost Analysis** and the dashboard KPI cards.
