import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# ----------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------
st.set_page_config(page_title="Student Stress Monitoring", layout="wide")

# *** IMPORTANT ***
# This URL must point to your deployed FastAPI backend.
# For local testing, it's: "http://127.0.0.1:8000"
API_URL = "http://127.0.0.1:8000"

# ----------------------------------------------------------
# LOAD STATIC DATA (MODIFIED)
# ----------------------------------------------------------
st.title("📊 Student Stress Detection & Monitoring System")
st.write("""
This interactive system predicts student stress levels using a **ML/AI backend**
and provides **AI-generated insights** to help interpret contributing factors.
""")

# --- NEW: Function to load monitoring data from the API ---
@st.cache_data(ttl=300) # Cache for 5 minutes
def load_data_from_api():
    """
    Fetches the main dataset from the /monitoring-data endpoint.
    This is used by the 'Dataset & Monitoring' page.
    """
    try:
        response = requests.get(f"{API_URL}/monitoring-data")
        response.raise_for_status()
        # Convert list of dicts from API to DataFrame
        return pd.DataFrame(response.json())
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Connection Error: Could not load monitoring data from API at {API_URL}/monitoring-data. Is the backend running?")
        return pd.DataFrame() # Return empty dataframe
    except Exception as e:
        st.error(f"❌ Error loading data from API: {e}")
        return pd.DataFrame()

# --- MODIFIED: Load local CSV primarily for form generation ---
try:
    # We still load the local CSV to get the column names and unique
    # values for the input form on the 'Prediction' page.
    data_for_form = pd.read_csv("Dataset/StressLevelDataset.csv")
    X = data_for_form.drop("stress_level", axis=1)
    y = data_for_form["stress_level"]
except FileNotFoundError:
    st.error("❌ Missing required file: 'Dataset/StressLevelDataset.csv'.")
    st.write("This file is still needed to generate the input form fields.")
    st.stop()


# ----------------------------------------------------------
# STEP 3: Sidebar Navigation
# ----------------------------------------------------------
st.sidebar.title("📌 Navigation")

if "page" not in st.session_state:
    st.session_state.page = "Scaling or Chart"

nav_buttons = [
    ("📏 Scaling or Chart", "Scaling or Chart"),
    ("🧑‍🎓 Student Input & Prediction", "Student Input & Prediction"),
    ("📈 Dataset & Monitoring", "Dataset & Monitoring"),
    ("🤖 AI Chatbot", "AI Chatbot")
]

for label, page_name in nav_buttons:
    if st.sidebar.button(label):
        st.session_state.page = page_name

page = st.session_state.page

# ----------------------------------------------------------
# STEP 4: Helper Data
# ----------------------------------------------------------
stress_labels = {0: "Low Stress", 1: "Medium Stress", 2: "High Stress"}
input_descriptions = {
    "anxiety_level": "Higher values indicate more anxiety (0-21)",
    "self_esteem": "Higher values indicate stronger self-esteem (0-30)",
    "mental_health_history": "1 = has a history, 0 = none",
    "depression": "Higher values indicate more symptoms (0-27)",
    "headache": "Frequency/severity (0-5)",
    "blood_pressure": "1 = normal, 2-3 = elevated/high",
    "sleep_quality": "1 = very poor, 5 = very good",
    "breathing_problem": "Severity (0-5)",
    "noise_level": "Exposure to noise (0-5)",
    "living_conditions": "Higher = better comfort (0-5)",
    "safety": "Perceived safety (0-5)",
    "basic_needs": "Fulfillment of needs (0-5)",
    "academic_performance": "Higher = better performance (0-5)",
    "study_load": "Higher = heavier workload (0-5)",
    "teacher_student_relationship": "Quality of relationship (0-5)",
    "future_career_concerns": "Level of worry (0-5)",
    "social_support": "Strength of support (0-3)",
    "peer_pressure": "Influence from peers (0-5)",
    "extracurricular_activities": "Involvement (0-5)",
    "bullying": "1 = none, higher = more bullying (0-5)"
}

# ----------------------------------------------------------
# PAGE 1: Feature Scaling or Chart
# ----------------------------------------------------------
if page == "Scaling or Chart":
    st.markdown("---")
    st.header("📏 Feature Scaling and Interpretation Chart")
    st.write("Standard scales used to interpret stress-related factors:")

    # --- Anxiety Scale ---
    st.subheader("🔹 Anxiety Level (0–21)")
    st.table(pd.DataFrame({
        "Score Range": ["0–4", "5–9", "10–14", "15–21"],
        "Description": ["Minimal Anxiety", "Mild", "Moderate", "Severe"],
        "Typical Effect on Stress": ["Low", "Moderate", "High", "Very High"]
    }))
    st.markdown("""
    🔗 **Check your Anxiety Level (GAD-7 Test)** 👉 [GAD-7 Calculator on MDCalc](https://www.mdcalc.com/calc/1727/gad7-general-anxiety-disorder7#next-steps)
    """)

    # --- Depression Scale ---
    st.markdown("---")
    st.subheader("🔹 Depression (0–27, PHQ-9)")
    st.table(pd.DataFrame({
        "Score Range": ["0–4", "5–9", "10–14", "15–19", "20–27"],
        "Description": ["Minimal", "Mild", "Moderate", "Moderately Severe", "Severe"],
        "Typical Effect on Stress": ["Low", "Mild", "Medium", "High", "Very High"]
    }))
    st.markdown("""
    🔗 **Check your Depression Severity (PHQ-9 Test)** 👉 [PHQ-9 Calculator on MDCalc](https://www.mdcalc.com/calc/1725/phq9-patient-health-questionnaire-9)
    """)

    # --- Self Esteem ---
    st.markdown("---")
    st.subheader("🔹 Self-Esteem (0–30)")
    st.table(pd.DataFrame({
        "Score Range": ["0–10", "11–20", "21–30"],
        "Description": ["Low", "Moderate", "High"],
        "Typical Effect on Stress": ["High vulnerability", "Moderate", "Protective"]
    }))

    # --- Blood Pressure ---
    st.markdown("---")
    st.subheader("🔹 Blood Pressure (0–3)")
    st.table(pd.DataFrame({
        "Value": [0, 1, 2, 3],
        "Description": ["Normal", "Elevated", "Stage 1", "Stage 2"],
        "Stress Impact": ["Low", "Moderate", "High", "Very High"]
    }))

    # --- Social Support ---
    st.markdown("---")
    st.subheader("🔹 Social Support (0–3)")
    st.table(pd.DataFrame({
        "Value": [0, 1, 2, 3],
        "Description": ["None", "Weak", "Good", "Strong"],
        "Stress Impact": ["Very High", "High", "Moderate", "Low"]
    }))

    # --- Likert ---
    st.markdown("---")
    st.subheader("🔹 Likert Scale (0–5)")
    st.table(pd.DataFrame({
        "Value": [0, 1, 2, 3, 4, 5],
        "Meaning": ["Very Low", "Low", "Slightly Low", "Moderate", "High", "Very High"]
    }))

    # --- Summary ---
    st.markdown("---")
    st.subheader("📊 Summary of Feature Effects")
    st.table(pd.DataFrame({
        "Feature": ["anxiety_level", "self_esteem", "mental_health_history", "depression", "blood_pressure", "social_support", "Likert (0–5)"],
        "Range": ["0–21", "0–30", "0–1", "0–27", "0–3", "0–3", "0–5"],
        "Interpretation": [
            "Emotional anxiety (GAD-7)", "Confidence/self-worth", "History of mental illness",
            "Depression severity (PHQ-9)", "Physiological stress", "Emotional & social backup",
            "Lifestyle & environmental factors"
        ],
        "Stress Effect": [
            "Higher = more stress", "Lower = more stress", "1 = more stress",
            "Higher = more stress", "Higher = more stress", "Lower = more stress", "Depends on factor type"
        ]
    }))

# ----------------------------------------------------------
# PAGE 2: Student Input & Prediction
# ----------------------------------------------------------
elif page == "Student Input & Prediction":
    st.markdown("---")
    st.subheader("🔹 Feature Scaling Reference")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔹 Anxiety Level (0–21)")
        st.table(pd.DataFrame({
            "Score Range": ["0–4", "5–9", "10–14", "15–21"],
            "Description": ["Minimal Anxiety", "Mild Anxiety", "Moderate Anxiety", "Severe Anxiety"],
            "Typical Effect on Stress": ["Low Stress", "Moderate Stress Risk", "Medium–High Stress", "High Stress"]
        }))
        st.markdown("""
        🔗 **Check your Anxiety Level (GAD-7 Test)** 👉 [GAD-7 Calculator on MDCalc](https://www.mdcalc.com/calc/1727/gad7-general-anxiety-disorder7#next-steps)
        """)

        st.subheader("🔹 Depression (0–27, PHQ-9)")
        st.table(pd.DataFrame({
            "Score Range": ["0–4", "5–9", "10–14", "15–19", "20–27"],
            "Description": ["Minimal", "Mild", "Moderate", "Moderately Severe", "Severe"],
            "Typical Effect on Stress": ["Low", "Mild", "Medium", "High", "Very High"]
        }))
        st.markdown("""
        🔗 **Check your Depression Severity (PHQ-9 Test)** 👉 [PHQ-9 Calculator on MDCalc](https://www.mdcalc.com/calc/1725/phq9-patient-health-questionnaire-9)
        """)

        st.markdown("**Self-Esteem (0–30)**")
        st.table(pd.DataFrame({
            "Range": ["0–10", "11–20", "21–30"],
            "Description": ["Low", "Moderate", "High"],
            "Stress Impact": ["High", "Moderate", "Low"]
        }))

    with col2:
        st.markdown("**Blood Pressure (0–3)**")
        st.table(pd.DataFrame({
            "Value": [0, 1, 2, 3],
            "Description": ["Normal", "Elevated", "Stage 1", "Stage 2"],
            "Stress Impact": ["Low", "Moderate", "High", "Very High"]
        }))

        st.markdown("**Social Support (0–3)**")
        st.table(pd.DataFrame({
            "Value": [0, 1, 2, 3],
            "Description": ["None", "Weak", "Good", "Strong"],
            "Stress Impact": ["Very High", "High", "Moderate", "Low"]
        }))

        st.markdown("**Likert Scale (0–5)**")
        st.table(pd.DataFrame({
            "Value": [0, 1, 2, 3, 4, 5],
            "Meaning": ["Very Low", "Low", "Slightly Low", "Moderate", "High", "Very High"]
        }))

    st.markdown("---")
    st.header("🧠 Stress Level Prediction")
    st.write("Provide your data below to predict your stress level:")

    user_inputs = {}
    # Use X.columns from the local CSV to generate the form
    for col in X.columns: 
        unique_vals = sorted(data_for_form[col].unique())
        default_val = int(data_for_form[col].median())
        user_inputs[col] = st.selectbox(
            f"{col} ({input_descriptions.get(col, '')})",
            unique_vals,
            index=unique_vals.index(default_val) if default_val in unique_vals else 0
        )

    if st.button("🔍 Predict Stress Level"):
        
        # Convert all values to standard Python int for JSON serialization
        payload_data = {}
        for key, value in user_inputs.items():
            payload_data[key] = int(value)

        try:
            # --- Call the Prediction API ---
            with st.spinner("Analyzing your data..."):
                pred_response = requests.post(f"{API_URL}/predict", json=payload_data)
                pred_response.raise_for_status() # Raise error for bad status
                pred_data = pred_response.json()

                label = pred_data["label"]
                factors = pred_data["factors"]
                
                st.success(f"🎯 Predicted Stress Level: **{label}**")
                st.info(f"📌 Main Factors: {', '.join(factors)}")

            # --- Call the Explanation API ---
            with st.spinner("Generating AI explanation..."):
                exp_payload = {"label": label, "factors": factors}
                exp_response = requests.post(f"{API_URL}/explain", json=exp_payload)
                exp_response.raise_for_status()
                exp_data = exp_response.json()
                
                st.markdown(f"📝 **Explanation:** {exp_data['explanation']}")

        except requests.exceptions.ConnectionError:
            st.error(f"❌ Connection Error: Could not connect to the AI/ML backend API at {API_URL}. Please ensure it's running.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# ----------------------------------------------------------
# PAGE 3: Dataset & Monitoring (MODIFIED)
# ----------------------------------------------------------
elif page == "Dataset & Monitoring":
    st.header("📈 Dataset & Model Monitoring")
    st.write("Displaying data fetched live from the API database.")

    # --- NEW: Load data from API ---
    monitoring_data = load_data_from_api()
    
    if not monitoring_data.empty:
        st.dataframe(monitoring_data.head(100))

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Stress Level Distribution (from DB)")
            fig, ax = plt.subplots()
            # Plot from the dataframe loaded from the API
            sns.countplot(x="stress_level", data=monitoring_data, ax=ax, palette="Set2")
            st.pyplot(fig)

        with col2:
            st.subheader("Model Evaluation")
            st.write("This section shows data from the *database*.")
            st.write(f"Total Rows in DB Table: {len(monitoring_data)}")
            
            # This part remains a placeholder as the API doesn't
            # provide a live classification report.
            st.subheader("Data Counts (from local CSV)")
            st.write(f"Total Rows (local): {len(data_for_form)}")
            st.write(f"Test Rows (20% local): {len(y[int(len(y)*0.8):])}")
            st.write(f"Train Rows (80% local): {len(y[:int(len(y)*0.8)])}")
            
    else:
        st.warning("Could not display monitoring data. Please check API connection.")


# ------------------------------
# 🤖 PAGE 5: AI Chatbot
# ------------------------------
elif page == "AI Chatbot":
    st.header("🤖 AI Stress Support Chatbot")
    st.write("Chat with a supportive AI designed to help students manage stress and wellbeing.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- Display chat history ---
    chat_container = st.container(height=400)
    with chat_container:
        for sender, msg in st.session_state.chat_history:
            if sender == "You":
                st.markdown(f"**🧑‍🎓 You:*** {msg}")
            else:
                st.markdown(f"**🤖 Bot:** {msg}")
            
    # --- Chat Input ---
    user_message = st.text_input("You:", key="chat_input")

    if st.button("Send") and user_message.strip():
        # Add user message to history
        st.session_state.chat_history.append(("You", user_message))
        
        # Prepare history for the API
        api_history = [msg for sender, msg in st.session_state.chat_history]

        try:
            with st.spinner("Thinking..."):
                # --- Call the Chat API ---
                chat_payload = {"message": user_message, "history": api_history}
                response = requests.post(f"{API_URL}/chat", json=chat_payload)
                response.raise_for_status()
                
                chat_data = response.json()
                
                final_reply = f"{chat_data['reply']}\n\n💡 *Advice:* {chat_data['advice']}"
                # Add bot reply to history
                st.session_state.chat_history.append(("Bot", final_reply))
                
                # Clear the input box by rerunning
                st.rerun()

        except requests.exceptions.ConnectionError:
            st.error(f"❌ Connection Error: Could not connect to the Chatbot API at {API_URL}. Please ensure it's running.")
            st.session_state.chat_history.pop() # Remove the user's message if send failed
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.chat_history.pop()