import pandas as pd
import os
from database import engine, Base, SessionLocal
from main import StudentRecord  # Import the Unified Model

csv_path = "Dataset/StressLevelDataset.csv"

if not os.path.exists(csv_path):
    print(f"❌ Error: File not found at {csv_path}")
    exit()

print("⏳ Reading CSV...")
df = pd.read_csv(csv_path)

# Reset Database
print("♻️  Resetting Database tables...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print(f"🧠 Processing {len(df)} records (calculating factors)...")
db = SessionLocal()
records_to_add = []

for _, row in df.iterrows():
    # 1. Calculate Factors (Same logic as main.py)
    factors = []
    if row.get('anxiety_level', 0) > 10: factors.append("High Anxiety")
    if row.get('sleep_quality', 0) < 3: factors.append("Poor Sleep")
    if row.get('study_load', 0) > 3: factors.append("Heavy Workload")
    if row.get('depression', 0) > 10: factors.append("Depression Symptoms")
    if row.get('social_support', 0) < 2: factors.append("Low Social Support")
    if row.get('bullying', 0) > 2: factors.append("Bullying")
    if not factors: factors.append("General Stress")

    # 2. Get Label
    stress_val = row.get('stress_level', 0)
    labels = {0: "Low Stress", 1: "Medium Stress", 2: "High Stress"}
    
    # 3. Create Record
    record_data = row.to_dict()
    new_record = StudentRecord(
        **record_data,
        predicted_label=labels.get(stress_val, "Unknown"),
        predicted_factors=", ".join(factors)
    )
    records_to_add.append(new_record)

# 4. Bulk Save
try:
    db.add_all(records_to_add)
    db.commit()
    print(f"✅ Success! Seeded {len(records_to_add)} records into 'student_records'.")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()
