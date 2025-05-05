# 💸 Personal Expense Tracker + ML Forecast

Track your expenses, store them securely in S3, and get monthly budget forecasts.

This project was created for training purposes as preparation for a company challenge covering the following topics:
- docker and docker-compose
- model deployment (Amazon EC2)
- AWS S3
- pandas
- pytest
- SQL
- Flask, fastAPI and REST API

Stil missing: **Amazon EC2**, **SQL**

## Features
- REST API with FastAPI
- ML Forecasting (3-month horizon)
- Docker + Pytest + Pandas
- Add and retrieve personal expenses via API  
- Store and read data from AWS S3 (CSV format)  
- Machine Learning-based forecasting (Linear Regression)  
- Streamlit dashboard for visual insights  
- Docker-ready for deployment  
- `.env` file for secure configuration


## File Structure

```text
expense-tracker/
├── app/
│   ├── main.py               # FastAPI app
│   ├── ml_model.py           # Forecasting logic
│   ├── s3_handler.py         # Save/load expenses in S3
│   ├── db.py                 # Save/load expenses in local CSV
│   ├── schemas.py            # Pydantic models
├── streamlit_app/
│   └── dashboard.py          # Optional frontend
├── tests/
│   └── test_app.py           # testing usecases 
├── models/          
│   └── model_LR.pkl          # Models saved
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## API Endpoints
```text
POST /add_expense/ → Add a new expense
GET /expenses/ → Get all expenses
GET /forecast/ → Monthly forecast
```

## Environment Setup

### 1. Clone the repo
```bash
git clone https://github.com/Nynor-code/personal-expense-tracking.git
cd personal-expense-tracking
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file from template
```bash
cp .env.example .env
```

Update it with your AWS credentials.

# 🔐 .env Configuration
```dotenv
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
S3_BUCKET_NAME=your_bucket
S3_KEY=expenses.csv
```

# 🧪 Run Locally
Open two terminals

## Flask API (terminal 1)
```bash
python src/main.py  # or make api
```

## Streamlit Dashboard (terminal 2)
```bash
streamlit run src/dashboard.py  # or make streamlit
```

# 🧪 Testing
```bash
pytest   # or make test
```

# 🐳 Docker
```bash
docker build -t expense-tracker .
docker run -p 5000:5000 --env-file .env expense-tracker
```

# 👩‍💻 Author
Created by [Nynor Pires](https://nynor-code.github.io/nfpires/)

# 📄 License
MIT License
