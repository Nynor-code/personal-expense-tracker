# src/ml_model.py
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_expenses(data: pd.DataFrame):
    data['date'] = pd.to_datetime(data['date'])
    data = data.groupby(pd.Grouper(key='date', freq='M')).sum().reset_index()
    data['timestamp'] = data['date'].astype(np.int64) // 10**9

    X = data[['timestamp']]
    y = data['amount']
    model = LinearRegression().fit(X, y)

    # Forecast next 3 months
    last_timestamp = data['timestamp'].max()
    next_ts = [last_timestamp + 2629743 * i for i in range(1, 4)]
    predictions = model.predict(np.array(next_ts).reshape(-1, 1))

    return {"forecast": list(predictions)}
