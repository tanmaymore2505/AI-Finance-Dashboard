import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
users = {"tanmay":"1234"}

st.sidebar.title("Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password",type="password")

if username in users and users[username] == password:
    st.sidebar.success("Logged In")

else:
    st.warning("Please login to use the dashboard")
    st.stop()

file = "expenses.csv"

# create csv if not exists
if not os.path.exists(file):
    df = pd.DataFrame(columns=["Date","Category","Amount","Description"])
    df.to_csv(file,index=False)

st.title("💰 AI Smart Expense Tracker Dashboard")

# load data
df = pd.read_csv(file)
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

# ---------------- ADD EXPENSE ----------------

st.header("Add Expense")

date = st.date_input("Date")
category = st.selectbox("Category",["Food","Travel","Shopping","Bills","Other"])
amount = st.number_input("Amount")
description = st.text_input("Description")

if st.button("Add Expense"):
    new_data = pd.DataFrame([[date,category,amount,description]],
    columns=["Date","Category","Amount","Description"])

    new_data.to_csv(file,mode="a",header=False,index=False)

    st.success("Expense Added Successfully")

# reload data
df = pd.read_csv(file)

# ---------------- SHOW DATA ----------------

st.header("Expense History")

st.dataframe(df)

# ---------------- TOTAL EXPENSE ----------------

total = df["Amount"].sum()
st.subheader(f"Total Spending: ₹{total}")

# ---------------- CATEGORY GRAPH ----------------

st.header("Category Spending Analysis")

category_total = df.groupby("Category")["Amount"].sum()

fig, ax = plt.subplots()
category_total.plot(kind="bar",ax=ax)
plt.title("Expenses by Category")
plt.ylabel("Amount")

st.pyplot(fig)

# ---------------- MONTHLY GRAPH ----------------

st.header("Monthly Spending")

df["Date"] = pd.to_datetime(df["Date"])

monthly = df.groupby(df["Date"].dt.month)["Amount"].sum()

fig2, ax2 = plt.subplots()
monthly.plot(kind="line",marker="o",ax=ax2)
plt.title("Monthly Expense Trend")

st.pyplot(fig2)

# ---------------- AI PREDICTION ----------------

st.header("AI Expense Prediction")

if len(df) > 5:

    df["Day"] = df["Date"].dt.day

    X = df[["Day"]]
    y = df["Amount"]

    model = LinearRegression()
    model.fit(X,y)

    future_day = np.array([[30]])
    prediction = model.predict(future_day)

    st.success(f"Predicted expense near end of month: ₹{prediction[0]:.2f}")

else:
    st.warning("Add more data for AI prediction")

# ---------------- BUDGET WARNING ----------------

st.header("Budget Monitor")

budget = st.number_input("Enter Monthly Budget")

if st.button("Check Budget"):

    if total > budget:
        st.error("⚠️ You exceeded your monthly budget!")
    else:
        st.success("You are within your budget")
st.header("AI Financial Advisor")

if len(df) > 0:

    category_total = df.groupby("Category")["Amount"].sum()

    highest_category = category_total.idxmax()
    highest_amount = category_total.max()

    st.write(f"You spend the most on **{highest_category}** (₹{highest_amount})")

    if highest_category == "Food":
        st.info("💡 Tip: Try cooking at home more often to save money.")

    elif highest_category == "Shopping":
        st.info("💡 Tip: Consider reducing unnecessary shopping expenses.")

    elif highest_category == "Travel":
        st.info("💡 Tip: Use public transport to reduce travel costs.")

    else:
        st.info("💡 Tip: Track your daily spending to optimize your budget.")