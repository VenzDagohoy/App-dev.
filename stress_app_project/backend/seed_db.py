import pandas as pd
import os
# Now this import works because we created database.py!
from database import engine, Base 

# 1. Load the CSV
csv_path = "Dataset/StressLevelDataset.csv"

if not os.path.exists(csv_path):
    print(f"❌ Error: File not found at {csv_path}")
    print("Please check that the 'Dataset' folder exists inside 'backend'.")
    exit()

print("⏳ Reading CSV...")
data = pd.read_csv(csv_path)
print(f"✅ Loaded {len(data)} rows.")

# 2. Create Tables (Ensures the DB file exists)
print("⏳ Connecting to Database...")
Base.metadata.create_all(bind=engine)

# 3. Insert Data
try:
    # This writes to a table named "student_data"
    data.to_sql("student_data", con=engine, if_exists="replace", index=False)
    print("✅ Success! Database seeded.")
except Exception as e:
    print(f"❌ Error seeding database: {e}")