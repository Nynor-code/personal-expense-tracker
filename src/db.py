# src/db.py
import pandas as pd
import os

DATA_PATH = "data/expenses.csv"

def save_expense(expense):
    df = pd.DataFrame([expense.dict()])
    if os.path.exists(DATA_PATH):
        df.to_csv(DATA_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(DATA_PATH, index=False)

def load_expenses():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=["date", "category", "amount"])
