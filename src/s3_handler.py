# src/s3_handler.py
import os
import io
import boto3
import pandas as pd
from dotenv import load_dotenv

# Loads variables from .env into environment
load_dotenv()

# Load environment variables
BUCKET = os.getenv("S3_BUCKET_NAME")
KEY = "data/expenses.csv"

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)


def save_expense_to_s3(expense) -> None:
    """
    Save a new expense entry to the S3 bucket.

    Parameters:
    - expense: a Pydantic model or dict-like object with `.dict()` method
    """
    # Load current data
    try:
        df = load_expenses_from_s3()
        new = pd.DataFrame([expense])
        df = pd.concat([df, new], ignore_index=True)

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        s3.put_object(Bucket=BUCKET, Key=KEY, Body=csv_buffer.getvalue())
    except Exception as e:
        raise RuntimeError(f"Failed to save expense: {e}")


def load_expenses_from_s3() -> pd.DataFrame:
    '''
    Load expenses from the S3 bucket.
    Returns:
    - DataFrame: A pandas DataFrame containing the expenses.
    '''
    try:
        response = s3.get_object(Bucket=BUCKET, Key=KEY)
        return pd.read_csv(io.BytesIO(response['Body'].read()))
    except s3.exceptions.NoSuchKey:
        return pd.DataFrame()
    except Exception as e:
        raise RuntimeError(f"Failed to load expenses: {e}")
