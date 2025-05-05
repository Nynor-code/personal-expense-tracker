# app/main.py
from src.db import save_expense, load_expenses
from src.ml_model import forecast_expenses
from src.s3_handler import save_expense_to_s3, load_expenses_from_s3
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os


# Loads variables from .env into environment
load_dotenv()
# Load environment variables
USE_S3 = os.getenv("USE_S3")


app = Flask(__name__)
CORS(app)  # Allow frontend to access backend


if USE_S3:   # Check if we are using S3
    sv_expense = save_expense_to_s3
    ld_expenses = load_expenses_from_s3
else:
    sv_expense = save_expense
    ld_expenses = load_expenses

# Define the required fields for the expense

REQUIRED_FIELDS = ["date", "category", "amount",
                   "payment_method", "description"]


@app.route("/add_expense/", methods=["POST"])
def add_expense():
    data = request.get_json()
    if not all(field in data for field in REQUIRED_FIELDS):
        return jsonify({"error": "Missing required fields"}), 400
    sv_expense(data)
    return jsonify({"status": "Expense Saved"}), 200


@app.route("/expenses/", methods=["GET"])
def get_expenses():
    df = ld_expenses()
    return jsonify(df.to_dict(orient="records"))


@app.route("/forecast/", methods=["GET"])
def forecast():
    data = ld_expenses()
    return forecast_expenses(data)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
