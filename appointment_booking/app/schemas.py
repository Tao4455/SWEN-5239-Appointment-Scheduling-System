from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class AppointmentCreate(BaseModel):
    provider_id: int
    client_name: str
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = None

    @field_validator("end_time")
    @classmethod
    def validate_time(cls, end_time, info):
        start_time = info.data.get("start_time")
        if start_time and end_time <= start_time:
            raise ValueError("End time must be after start time")
        return end_time


class AppointmentResponse(BaseModel):
    id: int
    provider_id: int
    client_name: str
    start_time: datetime
    end_time: datetime
    notes: Optional[str]

    class Config:
        from_attributes = True
