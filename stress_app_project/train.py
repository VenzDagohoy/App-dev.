import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

print("Starting model training...")

# Load the dataset
try:
    # UPDATED PATH: Looking for the file in the 'Dataset' folder
    data = pd.read_csv("Dataset/StressLevelDataset.csv")
except FileNotFoundError:
    print("Error: StressLevelDataset.csv not found.")
    print("Please make sure 'StressLevelDataset.csv' is in the 'Dataset' folder.")
    exit()

if "stress_level" not in data.columns:
    print("Error: The file must contain a 'stress_level' column.")
    exit()

# Prepare data
X = data.drop("stress_level", axis=1)
y = data["stress_level"]

# Split data (using the same random_state as your app)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

print(f"Model trained with accuracy: {model.score(X_test, y_test):.4f}")

# Save the trained model to a file
joblib.dump(model, "stress_model.joblib")

print(f"Model successfully saved as 'stress_model.joblib'")