# src/db.py
import pandas as pd
import os

DATA_PATH = "data/expenses.csv"


def save_expense(expense):
    """
    Save a new expense entry to the local CSV file.
    Parameters:
    - expense: a Pydantic model or dict-like object with `.dict()` method
    """
    if os.path.exists(DATA_PATH):
        expense.to_csv(DATA_PATH, mode='a', header=False, index=False)
    else:
        expense.to_csv(DATA_PATH, index=False)


def load_expenses():
    ''' Load the expenses DataFrame from the local CSV file.'''
    # Check if the file exists
    # If it does, read it into a DataFrame
    # If it doesn't, return an empty DataFrame with the correct columns

    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        return pd.DataFrame(columns=[
            "date", "category", "amount",
            "payment_method", "description"
                                    ])
