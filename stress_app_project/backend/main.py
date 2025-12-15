from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
import joblib
import pandas as pd
import uvicorn
import os

# --- NEW: IMPORT SHARED DATABASE LOGIC ---
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base  

# --- APP CONFIGURATION ---
app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE MODEL (The Table Structure) ---
class StudentRecord(Base):
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, index=True)
    # Inputs
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
    # Outputs (Results)
    predicted_label = Column(String)
    predicted_factors = Column(String) 

# --- GLOBAL VARIABLES ---
model = None      # Random Forest (Score)
text_gen = None   # TinyLlama (Unified Brain)

# --- PYDANTIC MODELS ---
class StudentData(BaseModel):
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

class ExplanationInput(BaseModel):
    label: str
    factors: list

class ChatInput(BaseModel):
    message: str
    history: list

# --- HELPER: GET DATABASE SESSION ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- STARTUP: LOAD MODELS & CREATE DB ---
@app.on_event("startup")
async def startup_event():
    global model, text_gen
    
    print("⏳ Starting System...")

    # 1. Create Database Tables (Uses the shared 'Base' and 'engine')
    Base.metadata.create_all(bind=engine)
    print("✅ Database Tables Verified/Created!")

    # 2. Load Prediction Model
    try:
        if os.path.exists("stress_model.joblib"):
            model = joblib.load("stress_model.joblib")
            print("✅ Stress Model Loaded!")
        else:
            print("⚠️ stress_model.joblib not found.")
    except Exception as e:
        print(f"❌ Error loading stress model: {e}")

    # 3. Load Unified AI Brain
    print("⏳ Loading AI Brain (TinyLlama)...")
    try:
        text_gen = pipeline(
            "text-generation", 
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
            torch_dtype="auto"
        )
        print("✅ AI Brain Loaded Successfully!")
    except Exception as e:
        print(f"❌ Error loading AI: {e}")

# --- ROUTES ---
@app.get("/")
def read_root():
    return {"status": "Active", "mode": "Unified TinyLlama + Shared Database"}

@app.post("/predict")
def predict_stress(data: StudentData, db: Session = Depends(get_db)):
    if not model: raise HTTPException(status_code=503, detail="Model not loaded")
    
    input_df = pd.DataFrame([data.dict()])
    prediction = int(model.predict(input_df)[0])
    labels = {0: "Low Stress", 1: "Medium Stress", 2: "High Stress"}
    label = labels.get(prediction, "Unknown")
    
    factors = []
    if data.anxiety_level > 10: factors.append("High Anxiety")
    if data.sleep_quality < 3: factors.append("Poor Sleep")
    if data.study_load > 3: factors.append("Heavy Workload")
    if data.depression > 10: factors.append("Depression Symptoms")
    if data.social_support < 2: factors.append("Low Social Support")
    if data.bullying > 2: factors.append("Bullying")
    if not factors: factors.append("General Stress")

    # SAVE TO DATABASE
    try:
        new_record = StudentRecord(
            **data.dict(),
            predicted_label=label,
            predicted_factors=", ".join(factors)
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        print(f"✅ Saved Record ID: {new_record.id}")
    except Exception as e:
        print(f"❌ Database Save Error: {e}")

    return {"prediction": prediction, "label": label, "factors": factors}

@app.post("/explain")
async def get_explanation(input_data: ExplanationInput):
    if not text_gen: return {"explanation": "AI offline."}
    
    prompt = (
        f"<|system|>\n"
        f"You are a supportive and empathetic student wellness counselor. "
        f"Your goal is to explain stress factors clearly and offer 2 practical, non-medical tips. "
        f"Keep your response concise (under 100 words) and encouraging.</s>\n"
        f"<|user|>\n"
        f"I am a student predicted to have '{input_data.label}'. "
        f"My main stressors are: {', '.join(input_data.factors)}. "
        f"Can you explain why this interacts and what I should do?</s>\n"
        f"<|assistant|>\n"
    )

    try:
        output = text_gen(prompt, max_new_tokens=500, 
                          do_sample=True, 
                          temperature=0.7, 
                          repetition_penalty=1.2)[0]['generated_text']
        return {"explanation": output.split("<|assistant|>\n")[-1].strip()}
    except Exception:
        return {"explanation": "Focus on deep breathing."}

@app.post("/chat")
async def chat_endpoint(input_data: ChatInput):
    if not text_gen: return {"reply": "I'm offline.", "advice": "Check server."}
    recent_history = input_data.history[-4:]
    conversation_text = "\n".join(recent_history)

    prompt = (
        f"<|system|>\n"
        f"You are MindEase, a warm, empathetic AI therapist. "
        f"Your goal is to listen, validate feelings, and offer gentle support. "
        f"Keep answers short (2-3 sentences). Do not be robotic.</s>\n"
        f"<|user|>\n"
        f"Current Conversation:\n{conversation_text}\n"
        f"User: {input_data.message}</s>\n"
        f"<|assistant|>\n"
    )

    try:
        response = text_gen(prompt, max_new_tokens=250, do_sample=True, temperature=0.8, repetition_penalty=1.2)[0]['generated_text']
        reply = response.split("<|assistant|>\n")[-1].strip()
    except Exception:
        reply = "I'm listening."
    return {"reply": reply, "advice": "Active Listening"}

@app.get("/monitoring-data")
def get_monitoring_data(db: Session = Depends(get_db)):
    records = db.query(StudentRecord).all()
    return [{"id": r.id, "predicted_label": r.predicted_label, "anxiety_level": r.anxiety_level, "sleep_quality": r.sleep_quality, "study_load": r.study_load} for r in records]

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)