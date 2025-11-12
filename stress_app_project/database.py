from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Database Connection (using SQLite)
# This will create a file named 'student_stress.db' in your project directory
SQLALCHEMY_DATABASE_URL = "sqlite:///./student_stress.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Create SQLAlchemy Model (Table) for the original dataset
class StudentData(Base):
    __tablename__ = "student_data"
    
    id = Column(Integer, primary_key=True, index=True)
    anxiety_level = Column(Integer)
    self_esteem = Column(Integer)
    mental_health_history = Column(Integer)
    depression = Column(Integer)
    headache = Column(Integer)
    blood_pressure = Column(Integer)
    sleep_quality = Column(Integer)
    breathing_problem = Column(Integer)
    noise_level = Column(Integer)
    living_conditions = Column(Integer)
    safety = Column(Integer)
    basic_needs = Column(Integer)
    academic_performance = Column(Integer)
    study_load = Column(Integer)
    teacher_student_relationship = Column(Integer)
    future_career_concerns = Column(Integer)
    social_support = Column(Integer)
    peer_pressure = Column(Integer)
    extracurricular_activities = Column(Integer)
    bullying = Column(Integer)
    stress_level = Column(Integer) # Original target variable

# 3. Create SQLAlchemy Model (Table) for storing new predictions
class PredictionHistory(Base):
    __tablename__ = "prediction_history"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Store all the inputs
    anxiety_level = Column(Integer)
    self_esteem = Column(Integer)
    mental_health_history = Column(Integer)
    depression = Column(Integer)
    headache = Column(Integer)
    blood_pressure = Column(Integer)
    sleep_quality = Column(Integer)
    breathing_problem = Column(Integer)
    noise_level = Column(Integer)
    living_conditions = Column(Integer)
    safety = Column(Integer)
    basic_needs = Column(Integer)
    academic_performance = Column(Integer)
    study_load = Column(Integer)
    teacher_student_relationship = Column(Integer)
    future_career_concerns = Column(Integer)
    social_support = Column(Integer)
    peer_pressure = Column(Integer)
    extracurricular_activities = Column(Integer)
    bullying = Column(Integer)
    
    # Store the results
    predicted_label = Column(String)
    predicted_factors = Column(String) # Storing factors as comma-separated string

# 4. Helper function to get a DB session in API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()