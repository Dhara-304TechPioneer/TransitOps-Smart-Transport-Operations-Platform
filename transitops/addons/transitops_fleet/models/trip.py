from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TransitOpsTrip(models.Model):
    _name = "transitops.trip"
    _description = "TransitOps Trip"

    source = fields.Char(string="Source", required=True)
    destination = fields.Char(string="Destination", required=True)
    vehicle_id = fields.Many2one(
        comodel_name="transitops.vehicle",
        string="Vehicle",
    )
    driver_id = fields.Many2one(
        comodel_name="transitops.driver",
        string="Driver",
    )
    cargo_weight_kg = fields.Float(string="Cargo Weight (kg)")
    planned_distance_km = fields.Float(string="Planned Distance (km)")
    fuel_consumed = fields.Float(string="Fuel Consumed")
    final_odometer = fields.Float(string="Final Odometer")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("dispatched", "Dispatched"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        string="State",
        default="draft",
    )

    @api.constrains("cargo_weight_kg", "vehicle_id")
    def _check_cargo_weight_capacity(self):
        for trip in self:
            trip._validate_cargo_weight_capacity()

    @api.constrains("driver_id")
    def _check_driver_license_expiry(self):
        for trip in self:
            trip._validate_driver_license_expiry()

    def _validate_cargo_weight_capacity(self):
        self.ensure_one()
        if self.vehicle_id and self.cargo_weight_kg > self.vehicle_id.max_load_kg:
            raise ValidationError("Cargo weight cannot exceed vehicle maximum load capacity.")

    def _validate_driver_license_expiry(self):
        self.ensure_one()
        if self.driver_id.license_expiry and self.driver_id.license_expiry < fields.Date.today():
            raise ValidationError("Driver license has expired.")

    def action_dispatch(self):
        for trip in self:
            if not trip.vehicle_id:
                raise ValidationError("Vehicle is required to dispatch a trip.")
            if not trip.driver_id:
                raise ValidationError("Driver is required to dispatch a trip.")
            if trip.vehicle_id.status != "available":
                raise ValidationError("Vehicle must be available to dispatch a trip.")
            if trip.driver_id.status == "suspended":
                raise ValidationError("Suspended drivers cannot be dispatched.")
            if trip.driver_id.status != "available":
                raise ValidationError("Driver must be available to dispatch a trip.")
            trip._validate_driver_license_expiry()
            trip._validate_cargo_weight_capacity()

            trip.vehicle_id.status = "on_trip"
            trip.driver_id.status = "on_trip"
            trip.state = "dispatched"

    def action_complete(self):
        for trip in self:
            if trip.state != "dispatched":
                raise ValidationError("Only dispatched trips can be completed.")

            trip.vehicle_id.status = "available"
            trip.driver_id.status = "available"
            trip.state = "completed"

    def action_cancel(self):
        for trip in self:
            if trip.state not in ("draft", "dispatched"):
                raise ValidationError("Only draft or dispatched trips can be cancelled.")

            if trip.state == "dispatched":
                trip.vehicle_id.status = "available"
                trip.driver_id.status = "available"

            trip.state = "cancelled"
