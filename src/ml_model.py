# src/ml_model.py
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import pickle


def forecast_expenses(data: pd.DataFrame):
    data['date'] = pd.to_datetime(data['date'])
    data = data.groupby(pd.Grouper(key='date', freq='ME')).sum().reset_index()
    data['timestamp'] = data['date'].astype(np.int64) // 10**9

    X = data[['timestamp']]
    y = data['amount']
    model = LinearRegression().fit(X, y)

    # save and read the model
    with open('models/model_LR.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/model_LR.pkl', 'rb') as f:
        model = pickle.load(f)

    # Forecast next 3 months
    last_timestamp = data['timestamp'].max()
    next_ts = [last_timestamp + 2629743 * i for i in range(1, 4)]
    # 2629743 seconds is approximately 1 month
    # predict the next 3 months
    predictions = model.predict(np.array(next_ts).reshape(-1, 1))
    # present predictions in a readable format month:value
    predictions = {pd.to_datetime(ts, unit='s').strftime('%Y-%m'): pred
                   for ts, pred in zip(next_ts, predictions)
                   }
    predictions = {k: round(v, 2) for k, v in predictions.items()}

    return {"forecast": predictions}
