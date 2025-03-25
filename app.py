import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Smart Expense Tracker (₹)", layout="wide")

st.title("💰 Smart Expense Tracker (₹)")
st.write("Track your expenses with detailed insights!")

st.sidebar.header("📌 Add New Expense")

amount = st.sidebar.number_input("💵 Enter Amount (₹)", min_value=1.0, format="%.2f")
category = st.sidebar.text_input("📂 Enter Category")
description = st.sidebar.text_area("📝 Enter Description")
date = st.sidebar.date_input("📅 Date of Expense", datetime.today()).strftime("%Y-%m-%d")
payment_method = st.sidebar.selectbox("💳 Payment Method", ["Cash", "Card", "UPI", "Bank Transfer"])
location = st.sidebar.text_input("📍 Location (Optional)", "Unknown")

if st.sidebar.button("➕ Add Expense"):
    if category.strip() == "":
        st.sidebar.warning("⚠️ Please enter a category!")
    else:
        response = requests.post("http://127.0.0.1:8000/add_expense/", 
                                 params={
                                     "amount": amount,
                                     "category": category,
                                     "description": description,
                                     "date": date,
                                     "payment_method": payment_method,
                                     "location": location
                                 })
        if response.status_code == 200:
            st.sidebar.success("✅ Expense added successfully!")
        else:
            st.sidebar.error("⚠️ Error adding expense!")

st.header("📊 Expense Overview")

expense_data = requests.get("http://127.0.0.1:8000/get_expenses/").json()
analysis_data = requests.get("http://127.0.0.1:8000/analysis/").json()

if "expenses" in expense_data and expense_data["expenses"]:
    df = pd.DataFrame(expense_data["expenses"])
    st.dataframe(df, use_container_width=True)

    st.subheader("💵 Total Spent")
    st.metric(label="Total Spent", value=analysis_data["Total Spent"])

    st.subheader("📊 Spending by Category")
    category_spending = analysis_data["Category Wise Spending"]
    
    if category_spending:
        df_category = pd.DataFrame(list(category_spending.items()), columns=["Category", "Amount"])
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(df_category["Category"], df_category["Amount"], color="skyblue")
        ax.set_ylabel("Amount Spent (₹)")
        ax.set_xlabel("Category")
        ax.set_title("Total Spending by Category")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    st.subheader("🍰 Spending Distribution")
    category_percentage = analysis_data["Category Percentage"]
    if category_percentage:
        fig, ax = plt.subplots()
        ax.pie(category_spending.values(), labels=category_spending.keys(), autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
        ax.set_title("Category-Wise Spending")
        st.pyplot(fig)

    st.subheader("📈 Spending Trends")
    st.info("📅 Monthly and Weekly spending insights will be added soon!")

else:
    st.warning("🚀 No expenses recorded yet. Start by adding some!")
