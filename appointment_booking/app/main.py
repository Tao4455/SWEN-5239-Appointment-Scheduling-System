import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import Form
from datetime import datetime
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles




models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Appointment Booking System")

# HTML and CSS styles
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Clients create their appointment and verify them
@app.post("/appointments/", response_model=schemas.AppointmentResponse, status_code=201)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
):
    db_appointment = crud.create_appointment(db, appointment)

    if db_appointment is None:
        raise HTTPException(
            status_code=400,
            detail="Appointment time conflicts with an existing appointment."
        )

    return db_appointment

@app.get("/appointments/{provider_id}", response_model=List[schemas.AppointmentResponse])
def list_appointments(provider_id: int, db: Session = Depends(get_db)):
    return crud.get_appointments_by_provider(db, provider_id)


@app.get("/ui/{provider_id}", response_class=HTMLResponse)
def appointment_ui(request: Request, provider_id: int, db: Session = Depends(get_db)):
    appointments = crud.get_appointments_by_provider(db, provider_id)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "appointments": appointments,
            "provider_id": provider_id,
        },
    )


@app.post("/ui/appointments")
def create_appointment_form(
    request: Request,
    provider_id: int = Form(...),
    client_name: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    notes: str = Form(None),
    db: Session = Depends(get_db),
):
    appointment_data = schemas.AppointmentCreate(
        provider_id=provider_id,
        client_name=client_name,
        start_time=datetime.fromisoformat(start_time),
        end_time=datetime.fromisoformat(end_time),
        notes=notes,
    )

    db_appointment = crud.create_appointment(db, appointment_data)

    if db_appointment is None:
        appointments = crud.get_appointments_by_provider(db, provider_id)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "appointments": appointments,
                "provider_id": provider_id,
                "error": "Appointment time conflicts with an existing appointment."
            },
            status_code=400
    )


    return RedirectResponse(
        url=f"/ui/{provider_id}",
        status_code=303,
    )


@app.post("/ui/delete/{appointment_id}")
def delete_appointment_ui(
    request: Request,
    appointment_id: int,
    provider_id: int = Form(...),
    db: Session = Depends(get_db),
):
    success = crud.delete_appointment(db, appointment_id, provider_id)

    if not success:
        appointments = crud.get_appointments_by_provider(db, provider_id)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "appointments": appointments,
                "provider_id": provider_id,
                "error": "Appointment not found or unauthorized."
            },
            status_code=404
        )

    return RedirectResponse(
        url=f"/ui/{provider_id}",
        status_code=303
    )



@app.post("/ui/reschedule/{appointment_id}")
def reschedule_appointment(
    request: Request,
    appointment_id: int,
    provider_id: int = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    notes: str = Form(None),
    db: Session = Depends(get_db),
):
    updated = crud.update_appointment(
        db,
        appointment_id,
        provider_id,
        datetime.fromisoformat(start_time),
        datetime.fromisoformat(end_time),
        notes,
    )

    if updated is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if updated is False:
        appointments = crud.get_appointments_by_provider(db, provider_id)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "appointments": appointments,
                "provider_id": provider_id,
                "error": "Reschedule conflicts with another appointment."
            },
            status_code=400
        )

    return RedirectResponse(
        url=f"/ui/{provider_id}",
        status_code=303
    )