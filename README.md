# 💸 Personal Expense Tracker + ML Forecast

Track your expenses, store them securely in S3, and get monthly budget forecasts.

## Features
- REST API with FastAPI
- Data stored in AWS S3
- ML Forecasting (3-month horizon)
- Optional Streamlit Dashboard
- Docker + Pytest + Pandas

## API Endpoints
POST /add_expense/ → Add a new expense
GET /expenses/ → Get all expenses
GET /forecast/ → Monthly forecast


## Setup

```bash
git clone https://github.com/youruser/personal-expense-tracking.git
cd personal-expense-tracking
cp .env.template .env  # Fill in your AWS credentials
docker-compose up --build