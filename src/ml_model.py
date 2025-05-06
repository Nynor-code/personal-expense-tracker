# src/ml_model.py
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from datetime import timedelta


def forecast_expenses(data):
    '''
    Forecast the next 3 months of expenses using a linear regression model.

    Args:
        data (pd.DataFrame or list of dicts): The expenses data with:
        - date: The date of the expense (YYYY-MM-DD)
        - amount: The amount of the expense

    Returns:
        dict: Forecasted expenses for the next 3 months,
              with YYYY-MM keys and predicted amounts.
    '''
    df = pd.DataFrame(data)

    if df.empty or 'date' not in df.columns or 'amount' not in df.columns:
        return {"error": "Insufficient data for forecasting."}

    # Convert and clean data
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['date', 'amount']).sort_values('date')

    # Feature: days since first entry
    df['days'] = (df['date'] - df['date'].min()).dt.days
    X = df[['days']]
    y = df['amount']

    if len(df) < 2:
        return {"error": "Need at least two valid records to forecast."}

    # Train model
    model = LinearRegression().fit(X, y)

    # Forecast for the next 3 months (assume 30-day months)
    forecast = {}
    for i in range(1, 4):
        future_day = df['days'].max() + i * 30
        future_date = df['date'].max() + timedelta(days=i * 30)

        # FIX: ensure DataFrame input with correct column name
        pred = model.predict(pd.DataFrame([[future_day]], columns=['days']))[0]
        forecast[future_date.strftime('%Y-%m')] = round(pred, 2)

    # Save model (optional)
    with open('models/model_LR.pkl', 'wb') as f:
        pickle.dump(model, f)

    return forecast
