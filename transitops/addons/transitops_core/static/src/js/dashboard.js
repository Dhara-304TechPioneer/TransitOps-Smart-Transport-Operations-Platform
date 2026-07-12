/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onMounted, useState } from "@odoo/owl";

export class TransitOpsDashboard extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.state = useState({ data: null });

        onWillStart(async () => {
            this.state.data = await this.rpc("/transitops/dashboard_data", {});
        });

        onMounted(() => {
            this.loadChartJsAndRender();
        });
    }

    loadChartJsAndRender() {
        if (window.Chart) {
            this.renderChart();
            return;
        }
        
        const script = document.createElement("script");
        script.src = "https://cdn.jsdelivr.net/npm/chart.js";
        script.onload = () => {
            this.renderChart();
        };
        document.head.appendChild(script);
    }

    renderChart() {
        if (!this.state.data || !this.state.data.chart_data) return;
        
        const ctx = document.getElementById('tripChart');
        if (!ctx) return;

        new window.Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Draft', 'Dispatched', 'Completed', 'Cancelled'],
                datasets: [{
                    label: 'Trips by Status',
                    data: this.state.data.chart_data,
                    backgroundColor: [
                        '#17a2b8', // Info (Draft)
                        '#ffc107', // Warning (Dispatched)
                        '#28a745', // Success (Completed)
                        '#dc3545'  // Danger (Cancelled)
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }
}

TransitOpsDashboard.template = "transitops.Dashboard";

registry.category("actions").add("transitops.dashboard_action", TransitOpsDashboard);
