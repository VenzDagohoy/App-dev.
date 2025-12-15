from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Define the database file location
SQLALCHEMY_DATABASE_URL = "sqlite:///./student_stress.db"

# 2. Create the "Engine" (The core connection)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create the "Session" (How we talk to the db)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the "Base" (All models will inherit from this)
Base = declarative_base()
