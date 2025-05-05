# app/s3_handler.py
import boto3
import pandas as pd
import io
import os
from dotenv import load_dotenv

load_dotenv()


BUCKET = os.getenv("S3_BUCKET_NAME")
KEY = "expenses.csv"

s3 = boto3.client("s3")

def save_expense_to_s3(expense):
    try:
        df = load_expenses_from_s3()
    except:
        df = pd.DataFrame(columns=["date", "category", "amount"])

    new = pd.DataFrame([expense.dict()])
    df = pd.concat([df, new], ignore_index=True)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=BUCKET, Key=KEY, Body=csv_buffer.getvalue())

def load_expenses_from_s3():
    response = s3.get_object(Bucket=BUCKET, Key=KEY)
    return pd.read_csv(io.BytesIO(response['Body'].read()))
