from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import sqlite3

app = FastAPI()

# Load trained model
with open("expense_model.pkl", "rb") as f:
    model = pickle.load(f)

# Database connection
DB_FILE = "expenses.db"

class Expense(BaseModel):
    amount: float
    category: str
    description: str
    date: str
    payment_method: str
    location: str

@app.post("/add_expense/")
def add_expense(expense: Expense):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (amount, category, description, date, payment_method, location) VALUES (?, ?, ?, ?, ?, ?)",
                   (expense.amount, expense.category, expense.description, expense.date, expense.payment_method, expense.location))
    conn.commit()
    conn.close()
    return {"message": "Expense added successfully!"}

@app.get("/expenses/")
def get_expenses():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return [{"amount": row[1], "category": row[2], "description": row[3], "date": row[4], "payment_method": row[5], "location": row[6]} for row in expenses]

@app.post("/predict/")
def predict(amount: float):
    category = model.predict([[amount]])
    return {"Predicted Category": int(category[0])}
