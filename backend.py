from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import pandas as pd
from database import SessionLocal, Expense

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Welcome to the Smart Expense Tracker API"}

@app.post("/add_expense/")
def add_expense(amount: float, category: str, description: str, date: str, payment_method: str, location: str = "Unknown", db: Session = Depends(get_db)):
    expense = Expense(
        date=date, amount=amount, category=category,
        description=description, payment_method=payment_method,
        location=location
    )
    db.add(expense)
    db.commit()
    return {"message": "Expense added successfully!"}

@app.get("/get_expenses/")
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(Expense).all()
    return {"expenses": [expense.__dict__ for expense in expenses]}

@app.get("/analysis/")
def analysis(db: Session = Depends(get_db)):
    expenses = db.query(Expense).all()
    if not expenses:
        return {"message": "No expenses recorded yet."}

    df = pd.DataFrame([e.__dict__ for e in expenses])

    total_spent = df["amount"].sum()
    category_spending = df.groupby("category")["amount"].sum().to_dict()
    category_percentage = {cat: f"{(amt / total_spent) * 100:.2f}%" for cat, amt in category_spending.items()}

    return {
        "Total Spent": f"₹{total_spent:.2f}",
        "Category Wise Spending": category_spending,
        "Category Percentage": category_percentage,
        "Expense Count": len(expenses)
    }
