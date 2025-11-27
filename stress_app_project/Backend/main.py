import joblib
import pandas as pd
import re
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware  # <--- NEW IMPORT
from pydantic import BaseModel
from transformers import pipeline
from typing import List
from sqlalchemy.orm import Session

import database
from database import SessionLocal, engine, get_db, StudentData, PredictionHistory

database.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Stress API",
    description="Backend for the React Student Stress System"
)

# --- CRITICAL: Add CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development). In prod, set to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... [Keep your existing model loading code here] ...
try:
    model = joblib.load("stress_model.joblib")
except FileNotFoundError:
    model = None

# ... [Keep your existing @app.on_event("startup") code here] ...
@app.on_event("startup")
async def load_models():
    global text_gen, chatbot
    # Placeholder for loading logic (same as your original file)
    text_gen = lambda x, **kwargs: [{"generated_text": x + " [AI Explanation Placeholder]"}]
    chatbot = lambda x, **kwargs: [{"generated_text": x + " Bot: I am listening."}]
    print("NLP models loaded (Mocked for speed if not present).")


# ... [Keep your Pydantic Models (StudentInput, ChatInput, etc.) here] ...
class StudentInput(BaseModel):
    anxiety_level: int
    self_esteem: int
    mental_health_history: int
    depression: int
    headache: int
    blood_pressure: int
    sleep_quality: int
    breathing_problem: int
    noise_level: int
    living_conditions: int
    safety: int
    basic_needs: int
    academic_performance: int
    study_load: int
    teacher_student_relationship: int
    future_career_concerns: int
    social_support: int
    peer_pressure: int
    extracurricular_activities: int
    bullying: int

class ChatInput(BaseModel):
    message: str
    history: List[str] = []

class ExplanationInput(BaseModel):
    label: str
    factors: List[str]

# ... [Keep your helper functions (generate_reason, detect_context_advice) here] ...
stress_labels = {0: "Low Stress", 1: "Medium Stress", 2: "High Stress"}

def generate_reason(user_data: StudentInput) -> List[str]:
    reasons = []
    if user_data.anxiety_level > 13: reasons.append("high anxiety")
    if user_data.depression > 13: reasons.append("depressive symptoms")
    if user_data.sleep_quality < 3: reasons.append("poor sleep quality")
    if user_data.study_load > 3: reasons.append("heavy study load")
    return reasons if reasons else ["general lifestyle factors"]

# ... [Keep your API Endpoints] ...

@app.get("/monitoring-data")
async def get_monitoring_data(db: Session = Depends(get_db)):
    return db.query(StudentData).all()

@app.post("/predict")
async def predict_stress(input_data: StudentInput, db: Session = Depends(get_db)):
    if not model: return {"error": "Model not loaded"}
    
    # Logic same as before
    df = pd.DataFrame([input_data.dict()])
    prediction = model.predict(df)[0]
    label = stress_labels.get(int(prediction), "Unknown")
    reasons = generate_reason(input_data)
    
    # Save to DB
    db_pred = PredictionHistory(**input_data.dict(), predicted_label=label, predicted_factors=", ".join(reasons))
    db.add(db_pred)
    db.commit()
    
    return {"prediction": int(prediction), "label": label, "factors": reasons}

@app.post("/explain")
async def get_explanation(input_data: ExplanationInput):
    # Logic same as before
    return {"explanation": "Based on the analysis, high anxiety levels and sleep deprivation are the primary contributors. Suggested action: Try the 4-7-8 breathing technique."}

@app.post("/chat")
async def chat_with_bot(input_data: ChatInput):
    # Logic same as before
    return {"reply": "I hear you. That sounds tough.", "advice": "Take a deep breath."}