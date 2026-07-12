/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, xml } from "@odoo/owl";

class TransitOpsDashboard extends Component {}

TransitOpsDashboard.template = xml`
    <div class="o_transitops_dashboard p-4">
        <h1>TransitOps Dashboard</h1>
        <div class="row g-3 mt-1">
            <div class="col-12 col-md-6 col-xl-3">
                <div class="card"><div class="card-body">
                    <div class="text-muted">Total Vehicles</div><div class="h2 mb-0">—</div>
                </div></div>
            </div>
            <div class="col-12 col-md-6 col-xl-3">
                <div class="card"><div class="card-body">
                    <div class="text-muted">Available Vehicles</div><div class="h2 mb-0">—</div>
                </div></div>
            </div>
            <div class="col-12 col-md-6 col-xl-3">
                <div class="card"><div class="card-body">
                    <div class="text-muted">Vehicles On Trip</div><div class="h2 mb-0">—</div>
                </div></div>
            </div>
            <div class="col-12 col-md-6 col-xl-3">
                <div class="card"><div class="card-body">
                    <div class="text-muted">Vehicles In Maintenance</div><div class="h2 mb-0">—</div>
                </div></div>
            </div>
        </div>
    </div>`;

registry.category("actions").add("transitops_dashboard", TransitOpsDashboard);
