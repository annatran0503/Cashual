import streamlit as st
import pandas as pd
import numpy as np
import calendar
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load and display logo
st.title("\U0001F4CA Cashual - Spend Smart")

# User Input for Yearly and Monthly Budgeting
st.header("\U0001F4C5 Yearly and Monthly Budget Setup")
selected_year = st.selectbox("Select Year", list(range(2020, 2031)), index=4)
income = st.number_input("\U0001F4B0 Enter your monthly income:", min_value=0.0, value=3000.0, step=100.0)

# Fixed Monthly Costs Input
st.subheader("\U0001F4BC Enter Fixed Monthly Costs")
fixed_costs = {
    "Rent": st.number_input("Rent", min_value=0.0, value=1000.0, step=50.0),
    "Utilities": st.number_input("Utilities", min_value=0.0, value=200.0, step=10.0),
    "Subscriptions": st.number_input("Subscriptions (Netflix, Spotify, etc.)", min_value=0.0, value=50.0, step=5.0),
    "Insurance": st.number_input("Insurance", min_value=0.0, value=150.0, step=10.0),
    "Loan Payments": st.number_input("Loan Payments", min_value=0.0, value=300.0, step=20.0)
}

total_fixed_costs = sum(fixed_costs.values())
st.write(f"### \U0001F4B8 Total Fixed Costs: **${total_fixed_costs:,.2f}**")

# Remaining budget for daily spending
discretionary_income = income - total_fixed_costs
days_in_month = 30
daily_budget = discretionary_income / days_in_month
st.write(f"### \U0001F4C6 Daily Spending Budget: **${daily_budget:,.2f} per day**")

# Gamification - Rewards for staying under budget
st.subheader("🎮 Gamify Your Savings!")
st.write("Earn points for staying under your daily budget. Unlock badges as you save more!")

# Daily Spending Calendar Entry
st.header("📅 Daily Expense Tracker")
current_month = datetime.now().month
selected_month = st.selectbox("Select Month", list(calendar.month_name[1:]), index=current_month - 1)
selected_day = st.number_input("Select Day", min_value=1, max_value=31, value=datetime.now().day, step=1)

# Manual Expense Entry
df_daily_expenses = pd.DataFrame(columns=["Date", "Category", "Amount"])
categories = ["Groceries", "Transport", "Dining", "Entertainment", "Others"]
expense_category = st.selectbox("Select Category", categories)
expense_amount = st.number_input("Enter Expense Amount", min_value=0.0, value=0.0, step=1.0)

if st.button("Add Expense"):
    new_entry = pd.DataFrame({
        "Date": [f"{selected_year}-{selected_month}-{selected_day}"],
        "Category": [expense_category],
        "Amount": [expense_amount]
    })
    df_daily_expenses = pd.concat([df_daily_expenses, new_entry], ignore_index=True)
    st.success("Expense Added Successfully!")

# Show Daily Expenses
st.write("### 📝 Your Daily Expenses")
st.dataframe(df_daily_expenses)

# Check if daily budget is exceeded
total_spent_today = df_daily_expenses["Amount"].sum()
if total_spent_today > daily_budget:
    st.error(f"\U000026A0 You have overspent today! Spent: **${total_spent_today:,.2f}**, Budget: **${daily_budget:,.2f}**")
else:
    st.success(f"\U0001F44D You are within budget! Spent: **${total_spent_today:,.2f}**, Budget: **${daily_budget:,.2f}**")

# Display Badges
points = 0
if total_spent_today <= daily_budget:
    points += 10  # Reward points for staying under budget
    st.write(f"🎉 You've earned **{points} points** today!")

if points >= 50:
    st.write("🏆 **Silver Saver!** You've stayed under budget for 5 days!")
if points >= 100:
    st.write("🥇 **Gold Guru!** You've saved consistently for 10 days!")
if points >= 200:
    st.write("💎 **Diamond Master!** Your savings habits are top-tier!")

st.write("💡 Tip: Use the calendar to track your expenses daily!")
