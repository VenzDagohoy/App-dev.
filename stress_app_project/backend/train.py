import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from sqlalchemy import create_engine
from database import SQLALCHEMY_DATABASE_URL

print("Starting model training...")

try:
    # 1. Connect to the Database
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # 2. Read the Unified Table
    # We use "student_records" because that's the table name in main.py
    data = pd.read_sql_table("student_records", con=engine)
    
    print(f"Loaded {len(data)} rows from database.")

    # 3. CLEANING: Drop columns that are NOT numbers
    # The model crashes if it sees "High Stress" or "Anxiety, Sleep"
    cols_to_drop = ["id", "predicted_label", "predicted_factors", "stress_level"]
    
    # Define Features (X) -> All columns EXCEPT the ones above
    X = data.drop([c for c in cols_to_drop if c in data.columns], axis=1)
    
    # Define Target (y) -> The numeric stress score (0, 1, 2)
    if "stress_level" not in data.columns:
        print("❌ Error: 'stress_level' column is missing. Did you run seed_db.py?")
        exit()
        
    y = data["stress_level"]

except Exception as e:
    print(f"❌ Database Error: {e}")
    exit()

# 4. Split Data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train Model
print("🧠 Training Random Forest Model...")
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 6. Evaluate
accuracy = model.score(X_test, y_test)
print(f"✅ Model Accuracy: {accuracy:.4f}")

# 7. Save the Brain
joblib.dump(model, "stress_model.joblib")
print("✅ Model successfully saved as 'stress_model.joblib'")
