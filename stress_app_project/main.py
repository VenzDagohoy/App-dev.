import joblib
import pandas as pd
import re
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from typing import List

# ----------------------------------------------------------
# STEP 1: Initialize API and Load Models
# ----------------------------------------------------------

app = FastAPI(
    title="Student Stress API",
    description="Serves ML and NLP models for the stress monitoring system."
)

# --- Load ML Prediction Model (from Step 0) ---
try:
    model = joblib.load("stress_model.joblib")
except FileNotFoundError:
    print("FATAL ERROR: 'stress_model.joblib' not found.")
    print("Please run train.py first to create the model file.")
    model = None

# --- Load NLP Pipelines (Cached at startup) ---
@app.on_event("startup")
async def load_models():
    global text_gen, chatbot
    print("Loading NLP models... This may take a moment.")
    text_gen = pipeline("text-generation", model="openai-community/gpt2-medium")
    chatbot = pipeline("text-generation", model="microsoft/DialoGPT-small")
    print("NLP models loaded successfully.")

# ----------------------------------------------------------
# STEP 2: Define Data Input/Output Schemas (Pydantic)
# ----------------------------------------------------------

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

# --- NEW: Added this model for the /explain endpoint ---
class ExplanationInput(BaseModel):
    label: str
    factors: List[str]

class PredictionResponse(BaseModel):
    prediction: int
    label: str
    factors: List[str]

class ExplanationResponse(BaseModel):
    explanation: str
    
class ChatResponse(BaseModel):
    reply: str
    advice: str

# ----------------------------------------------------------
# STEP 3: Helper Functions
# ----------------------------------------------------------

stress_labels = {0: "Low Stress", 1: "Medium Stress", 2: "High Stress"}

def generate_reason(user_data: StudentInput) -> List[str]:
    """Generate logical explanations for predicted stress level."""
    reasons = []
    if user_data.anxiety_level > 13:
        reasons.append("high anxiety")
    if user_data.depression > 13:
        reasons.append("depressive symptoms")
    if user_data.sleep_quality < 3:
        reasons.append("poor sleep quality")
    if user_data.study_load > 3:
        reasons.append("heavy study load")
    if user_data.social_support < 2:
        reasons.append("weak social support")
    if user_data.bullying > 3:
        reasons.append("bullying experiences")
    if not reasons:
        reasons.append("balanced lifestyle with manageable factors")
    return reasons

def detect_context_advice(message: str) -> str:
    message = message.lower()
    advice_list = []
    # (Using the same regex logic from your script)
    if re.search(r"tired|exhausted|fatigue|sleepy|no energy", message):
        advice_list.append("Try keeping a consistent sleep schedule and take short relaxation breaks.")
    if re.search(r"anxious|nervous|panic|worried|fear", message):
        advice_list.append("Try deep breathing — inhale for 4 seconds, hold for 4, exhale for 6.")
    if re.search(r"depressed|sad|hopeless|down", message):
        advice_list.append("It might help to talk to someone you trust or engage in a relaxing activity.")
    if re.search(r"study|exam|school|assignment|workload", message):
        advice_list.append("Break your study sessions into smaller tasks with short breaks.")
    if re.search(r"overwhelmed|stress|pressure|burnout", message):
        advice_list.append("Pause for a few minutes and stretch or listen to calming music.")
    if not advice_list:
        advice_list.append("Take care of yourself — small breaks and mindful breathing can really help.")
    
    return " ".join(advice_list)

# ----------------------------------------------------------
# STEP 4: API Endpoints
# ----------------------------------------------------------

@app.get("/")
def read_root():
    return {"status": "Student Stress API is running."}

@app.post("/predict", response_model=PredictionResponse)
async def predict_stress(input_data: StudentInput):
    """Predicts stress level from student data."""
    if not model:
        return {"error": "ML Model not loaded."}
        
    # Convert Pydantic model to DataFrame for prediction
    user_data_df = pd.DataFrame([input_data.dict()])
    
    prediction = model.predict(user_data_df)[0]
    label = stress_labels.get(int(prediction), "Unknown")
    reasons = generate_reason(input_data)
    
    return {"prediction": int(prediction), "label": label, "factors": reasons}

# --- MODIFIED: Changed the function to accept the new ExplanationInput model ---
@app.post("/explain", response_model=ExplanationResponse)
async def get_explanation(input_data: ExplanationInput):
    """Generates an AI explanation for the prediction."""
    context = (
        f"The student has a predicted stress level of {input_data.label}. "
        f"Main influencing factors include {', '.join(input_data.factors)}. "
        "Write a clear, student-friendly explanation divided into two parts:\n\n"
        "### 🧠 Reasoning:\n"
        "- Describe in simple terms why these factors might lead to this stress level.\n\n"
        "### 💡 Suggestions:\n"
        "- Provide practical, encouraging, and non-medical advice for managing stress.\n"
        "- End with an empathetic, motivational message.\n"
    )

    ai_output = text_gen(
        context,
        max_new_tokens=200,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=50256
    )[0]['generated_text']
    
    explanation_text = ai_output[len(context):].strip()

    # Fallback text
    if not explanation_text or len(explanation_text) < 60:
        explanation_text = (
            "### 🧠 Reasoning:\n"
            "The student's current stress level appears to be influenced by emotional and lifestyle factors. "
            "High anxiety or poor sleep can make it difficult to concentrate.\n\n"
            "### 💡 Suggestions:\n"
            "Try maintaining a regular sleep schedule, take short breaks during study sessions, and seek support "
            "from friends or mentors. Small steps can make a big difference!"
        )
        
    return {"explanation": explanation_text}

@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(input_data: ChatInput):
    """Handles a single turn in the chatbot conversation."""
    
    # Generate keyword-based advice
    advice_text = detect_context_advice(input_data.message)
    
    # Generate conversational reply
    conversation = " ".join([f"User: {m}" if i % 2 == 0 else f"Bot: {m}" for i, m in enumerate(input_data.history[-3:])])
    conversation += f" User: {input_data.message}\nBot:"

    response = chatbot(
        conversation,
        max_new_tokens=80,
        pad_token_id=50256,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )[0]["generated_text"]
    
    bot_reply = response.split("Bot:")[-1].split("User:")[0].strip()
    bot_reply = re.sub(r"[\r\n]+", " ", bot_reply)
    bot_reply = bot_reply[:250].rsplit(".", 1)[0] + "." if len(bot_reply) > 250 else bot_reply

    if not bot_reply:
        bot_reply = "I'm here to listen. Tell me more about what’s been stressing you lately."
        
    return {"reply": bot_reply, "advice": advice_text}