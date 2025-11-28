import pandas as pd
from sqlalchemy import create_engine
from database import SQLALCHEMY_DATABASE_URL, Base, engine

# Get the original CSV dataset
try:
    data = pd.read_csv("Dataset/StressLevelDataset.csv")
except FileNotFoundError:
    print("Error: 'Dataset/StressLevelDataset.csv' not found.")
    print("Please make sure the file is in the 'Dataset' folder.")
    exit()

print(f"Loaded {len(data)} rows from CSV.")

# Create all tables (in case they don't exist)
Base.metadata.create_all(bind=engine)

# Use pandas.to_sql to insert the dataframe into the 'student_data' table
try:
    # 'if_exists='replace'' will drop the table first if it exists and create a new one.
    # Use 'if_exists='append'' if you want to add to existing data.
    data.to_sql("student_data", con=engine, if_exists="replace", index=False)
    print("Successfully populated the 'student_data' table in 'student_stress.db'.")
except Exception as e:
    print(f"Error writing to database: {e}")