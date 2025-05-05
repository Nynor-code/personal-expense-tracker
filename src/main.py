# app/main.py
from fastapi import FastAPI
from src.schemas import Expense
from src.db import save_expense, load_expenses
from src.ml_model import forecast_expenses

app = FastAPI()

@app.post("/add_expense/")
def add_expense(expense: Expense):
    save_expense(expense)
    return {"status": "ok"}

@app.get("/expenses/")
def get_expenses():
    return load_expenses()

@app.get("/forecast/")
def forecast():
    data = load_expenses()
    return forecast_expenses(data)
