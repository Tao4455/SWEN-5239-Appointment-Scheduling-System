

# ORM
# This file defines the structure of database tables
# using SQLAlchemy.
# Each class maps to a database table.




from sqlalchemy import Column, Integer, String, DateTime, Text
from .database import Base


# This is my database table, that consists of 6 entries, which match my user stories
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, nullable=False, index=True)
    client_name = Column(String(100), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    # Optional notes field (can be NULL)
    notes = Column(Text, nullable=True)
