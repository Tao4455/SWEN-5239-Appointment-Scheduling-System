
#Setting up the Database layer

# This file is responsible for:
# - Creating the database engine 
# - Creating sessions
# - Defining the Base class for ORM models
# ===================


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file.
DATABASE_URL = "sqlite:///./appointments.db"  # setting SQLite DB

#Set up my session factory and ORM base class 
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} # in case multiple threads may access the database.
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


Base = declarative_base()
