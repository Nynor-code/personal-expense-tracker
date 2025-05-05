'''
# streamlit_app/dashboard.py
This is the Streamlit dashboard for the Expense Tracker application.
It allows users to add expenses, view them, and see a forecast of future
expenses.
It interacts with a FastAPI backend to handle data storage and retrieval.
'''

import streamlit as st
import pandas as pd
import requests


st.title("💸 Expense Tracker + Forecast")

st.subheader("Add Expense")
with st.form(key="add_expense"):
    date = st.date_input("Date")
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0.0)
    payment_method = st.text_input("Payment Method")
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add")
    if submitted:
        res = requests.post("http://localhost:5000/add_expense/", json={
            "date": str(date),
            "category": category,
            "amount": amount,
            "payment_method": payment_method,
            "description": description
        })
        st.success(res.json()["status"])

st.subheader("📊 Expenses")
if st.button("Refresh"):
    res = requests.get("http://localhost:5000/expenses/")
    df = pd.DataFrame(res.json())
    st.dataframe(df)

st.subheader("🔮 Forecast")
try:
    res = requests.get("http://localhost:5000/forecast/")
    res.raise_for_status()
    forecast_data = res.json()["forecast"]

    # Convert dictionary to DataFrame properly

    df_forecast = pd.DataFrame(list(forecast_data.items()),
                               columns=["Month", "Forecast (€)"])

    st.write("### Next 3 Months Forecast")
    st.dataframe(df_forecast.style.format({"Forecast (€)": "€{:.2f}"}))

except requests.exceptions.RequestException as e:
    st.error(f"Could not connect to forecast API: {e}")
    forecast_data = None
