import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

API_URL = "http://127.0.0.1:8000/"

st.title("💰 Smart Expense Tracker")

# Add Expense Form
with st.form("add_expense"):
    amount = st.number_input("Enter Amount", min_value=1.0, format="%.2f")
    category = st.selectbox("Select Category", ["Food", "Transport", "Shopping", "Rent", "Bills", "Others"])
    description = st.text_area("Enter Description")
    date = st.date_input("Date of Expense")
    payment_method = st.selectbox("Payment Method", ["Cash", "Online"])
    location = st.text_input("Location (Optional)", "Unknown")

    submitted = st.form_submit_button("+ Add Expense")

    if submitted:
        data = {"amount": amount, "category": category, "description": description, "date": str(date),
                "payment_method": payment_method, "location": location}
        response = requests.post(f"{API_URL}add_expense/", json=data)
        if response.status_code == 200:
            st.success("✅ Expense added successfully!")
            st.experimental_rerun()

# Fetch Data
response = requests.get(f"{API_URL}expenses/")
if response.status_code == 200:
    expenses = response.json()
    
    if expenses:
        df = pd.DataFrame(expenses)

        # Convert date column to datetime
        df["date"] = pd.to_datetime(df["date"])

        # Show Data Table
        st.write("### 📋 Expense List")
        st.dataframe(df)

        # Expense Summary by Category (Bar Chart)
        st.write("### 📊 Expenses by Category")
        category_summary = df.groupby("category")["amount"].sum().reset_index()
        fig_bar = px.bar(category_summary, x="category", y="amount", color="category", title="Total Expenses by Category")
        st.plotly_chart(fig_bar)

        # Expense Trends Over Time (Line Chart)
        st.write("### 📈 Expense Trends Over Time")
        daily_expense = df.groupby("date")["amount"].sum().reset_index()
        fig_line = px.line(daily_expense, x="date", y="amount", title="Daily Expense Trends", markers=True)
        st.plotly_chart(fig_line)
    
    else:
        st.warning("⚠️ No expenses found. Add some first!")
else:
    st.error("❌ Failed to fetch expenses!")
