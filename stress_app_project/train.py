import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from sqlalchemy import create_engine
from database import SQLALCHEMY_DATABASE_URL # Import your DB URL

print("Starting model training...")

# --- NEW: Load data from database ---
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # Use pandas to read the entire 'student_data' table
    data = pd.read_sql_table("student_data", con=engine)
    
    # Drop the 'id' column as it's just the primary key
    if "id" in data.columns:
        data = data.drop("id", axis=1)
        
except Exception as e:
    print(f"Error: Could not read 'student_data' table from database.")
    print(f"Details: {e}")
    print("Please make sure the database is created and populated (run seed_db.py).")
    exit()

if "stress_level" not in data.columns:
    print("Error: The 'student_data' table must contain a 'stress_level' column.")
    exit()
# --- End of new data loading ---

# Prepare data
X = data.drop("stress_level", axis=1)
y = data["stress_level"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

print(f"Model trained with accuracy: {model.score(X_test, y_test):.4f}")

# Save the trained model to a file
joblib.dump(model, "stress_model.joblib")

print(f"Model successfully saved as 'stress_model.joblib'")