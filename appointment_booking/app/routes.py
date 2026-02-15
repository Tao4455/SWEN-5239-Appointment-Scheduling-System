from flask import Blueprint, request, jsonify
from datetime import datetime
from .database import db
from .models import Appointment
from .schemas import AppointmentSchema

appointments_bp = Blueprint("appointments", __name__)
appointment_schema = AppointmentSchema()

#Home Route
@appointments_bp.route("/", methods=["GET"])
def home():
    return {"message": "Appointment Booking API running"}, 200


@appointments_bp.route("/appointments", methods=["POST"])
def create_appointment():
    data = request.get_json()

    # Validate input
    errors = appointment_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    start_time = datetime.fromisoformat(data["start_time"])
    end_time = datetime.fromisoformat(data["end_time"])

    # Conflict detection
    overlapping = Appointment.query.filter(
        Appointment.start_time < end_time,
        Appointment.end_time > start_time
    ).first()

    if overlapping:
        return jsonify({"error": "Time slot already booked"}), 409

    appointment = Appointment(
        client_name=data["client_name"],
        service_type=data["service_type"],
        start_time=start_time,
        end_time=end_time
    )

    db.session.add(appointment)
    db.session.commit()

    return jsonify({"message": "Appointment created successfully"}), 201
