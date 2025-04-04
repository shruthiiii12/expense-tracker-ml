import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv("expenses.csv")

# Convert categories into numerical labels
df['Category'] = df['Category'].astype('category').cat.codes

# Features and target
X = df[['Amount']]
y = df['Category']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Save model
with open("expense_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained on a larger dataset!")

