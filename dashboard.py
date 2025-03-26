import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Set page config
st.set_page_config(page_title="Expense Tracker Dashboard", layout="wide")

st.title("📊 Expense Tracker Dashboard")

# Function to load expenses from SQLite database
def load_expenses():
    conn = sqlite3.connect("expenses.db")
    df = pd.read_sql("SELECT date, amount, category FROM expenses", conn)
    conn.close()

    # Convert to correct types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    
    return df

# Load data
df = load_expenses()

if df.empty:
    st.warning("⚠️ No expense data found. Please add expenses first.")
else:
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Expenses", f"${df['amount'].sum():.2f}")
    col2.metric("Average Expense", f"${df['amount'].mean():.2f}")
    col3.metric("Number of Transactions", len(df))

    # Expense Category Breakdown
    st.subheader("📌 Expense Category Breakdown")
    category_expense = df.groupby("category")["amount"].sum()

    if not category_expense.empty:
        fig, ax = plt.subplots()
        category_expense.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_ylabel("Amount ($)")
        st.pyplot(fig)
    else:
        st.warning("⚠️ No category-wise expenses available.")

    # Expense Trends Over Time
    st.subheader("📌 Expense Trends Over Time")
    if len(df) > 1:
        fig, ax = plt.subplots()
        df.sort_values("date", inplace=True)
        ax.plot(df["date"], df["amount"], marker="o", linestyle="-", color="green")
        ax.set_ylabel("Amount ($)")
        ax.set_xlabel("Date")
        st.pyplot(fig)
    else:
        st.warning("⚠️ Not enough data to display trends.")



