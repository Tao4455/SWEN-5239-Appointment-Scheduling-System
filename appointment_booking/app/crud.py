from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas
from datetime import datetime

# This is my logic layer that handles DB logic and routes to HTTP

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):

    overlapping_appointment = db.query(models.Appointment).filter(
        and_(
            models.Appointment.provider_id == appointment.provider_id,
            models.Appointment.start_time < appointment.end_time,
            models.Appointment.end_time > appointment.start_time
        )
    ).first()

    if overlapping_appointment:
        return None

    db_appointment = models.Appointment(
        provider_id=appointment.provider_id,
        client_name=appointment.client_name,
        start_time=appointment.start_time,
        end_time=appointment.end_time,
        notes=appointment.notes,
    )

    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointments_by_provider(db: Session, provider_id: int):
    return db.query(models.Appointment).filter(
        models.Appointment.provider_id == provider_id
    ).order_by(models.Appointment.start_time).all()


def delete_appointment(db: Session, appointment_id: int, provider_id: int):
    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id,
        models.Appointment.provider_id == provider_id
    ).first()

    if not appointment:
        return False

    db.delete(appointment)
    db.commit()
    return True

#Rescheule Feature based on our first Project
def update_appointment(db: Session, appointment_id: int, provider_id: int,
                       new_start: datetime, new_end: datetime, new_notes: str):

    appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id,
        models.Appointment.provider_id == provider_id
    ).first()

    if not appointment:
        return None

    overlapping = db.query(models.Appointment).filter(
        models.Appointment.provider_id == provider_id,
        models.Appointment.id != appointment_id,
        models.Appointment.start_time < new_end,
        models.Appointment.end_time > new_start
    ).first()

    if overlapping:
        return False

    appointment.start_time = new_start
    appointment.end_time = new_end
    appointment.notes = new_notes

    db.commit()
    db.refresh(appointment)
    return appointment