from sqlalchemy.orm import Session
from . import models
from datetime import datetime


# check to see if there is any overlapping schedules 
def is_overlapping(db: Session, start_time: datetime, end_time: datetime):
    return db.query(models.Appointment).filter(
        models.Appointment.start_time < end_time,
        models.Appointment.end_time > start_time
    ).first() is not None

# Function to create the appointments 
def create_appointment(db: Session, appointment):
    if is_overlapping(db, appointment.start_time, appointment.end_time):
        raise Exception("Appointment overlaps with an existing booking")
    
    # feel free to add more entries, there are just what I can think of ATM
    db_appointment = models.Appointment(
        client_name=appointment.client_name,
        start_time=appointment.start_time,
        end_time=appointment.end_time
    )

    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
