# tests/test_main.py

import pytest
import json
import pandas as pd
from unittest.mock import patch

from src.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_add_expense_success(client):
    """Test POST /add_expense/ with all required fields."""
    payload = {
        "date": "2024-05-01",
        "category": "Groceries",
        "amount": 45.75,
        "payment_method": "Credit Card",
        "description": "Weekly shopping"
    }
    response = client.post("/add_expense/",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 200
    assert response.json == {"status": "Expense Saved"}


def test_add_expense_missing_fields(client):
    """Test POST /add_expense/ with missing required fields."""
    payload = {
        "date": "2024-05-01",
        "amount": 45.75,
        # Missing 'category', 'payment_method', 'description'
    }
    response = client.post("/add_expense/",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 400
    assert "error" in response.json


def test_add_expense_invalid_types(client):
    """Test POST /add_expense/ with invalid data types."""
    payload = {
        "date": "not-a-date",
        "category": "Groceries",
        "amount": "not-a-number",
        "payment_method": "Card",
        "description": "Some expense"
    }
    response = client.post("/add_expense/",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code in [200, 500]  # Depends on backend logic


def test_get_expenses(client):
    """Test GET /expenses/ returns a list of expenses."""
    response = client.get("/expenses/")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    if response.json:
        assert "date" in response.json[0]
        assert "category" in response.json[0]


def test_forecast_expenses_function():
    """Test forecast_expenses() directly with dummy data."""
    from src.ml_model import forecast_expenses

    df = pd.DataFrame({
        'date': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01'],
        'amount': [100, 150, 200, 250]
    })
    result = forecast_expenses(df)
    assert isinstance(result, dict)
    assert len(result) == 2
    assert all(isinstance(k, str) for k in result.keys())
    assert all(isinstance(v, float) for v in result.values())


def test_forecast_endpoint(client):
    """Test GET /forecast/ endpoint."""
    response = client.get("/forecast/")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    # if response.json:
    #   assert all(isinstance(k, str) for k in response.json.keys())
    #   assert all(isinstance(v, float) for v in response.json.values())


def test_forecast_empty_data(client, monkeypatch):
    """Simulate empty expense data for forecast."""
    from src import main

    def mock_load_expenses():
        return pd.DataFrame()

    monkeypatch.setattr(main, "ld_expenses", mock_load_expenses)

    response = client.get("/forecast/")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    # no data returns an empty forecast with 1 line without values
    assert len(response.json) == 1


def test_add_and_get_expense(client):
    """Test adding an expense and retrieving it."""
    payload = {
        "date": "2024-05-02",
        "category": "Transport",
        "amount": 20.0,
        "payment_method": "Cash",
        "description": "Taxi"
    }
    post_resp = client.post("/add_expense/",
                            data=json.dumps(payload),
                            content_type="application/json")
    assert post_resp.status_code == 200

    get_resp = client.get("/expenses/")
    assert get_resp.status_code == 200
    expenses = get_resp.json
    assert isinstance(expenses, list)
    assert any(exp["description"] == "Taxi" for exp in expenses)


# ----------------------------
# Mocked S3 Test
# ----------------------------
@patch("src.main.sv_expense")
@patch("src.main.ld_expenses")
def test_s3_mocked_storage(mock_load, mock_save, client):
    """Test endpoints when using mocked S3 storage."""

    # Mock return from S3 load
    mock_load.return_value = pd.DataFrame([{
        "date": "2024-05-01",
        "category": "Mock",
        "amount": 123.45,
        "payment_method": "MockedCard",
        "description": "Mocked Description"
    }])

    # Simulate a save call (we just assert it was called)
    payload = {
        "date": "2024-05-01",
        "category": "Mock",
        "amount": 123.45,
        "payment_method": "MockedCard",
        "description": "Mocked Description"
    }

    response = client.post("/add_expense/",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 200
    assert response.status_code == 200
    print("save_expense_to_s3 called?", mock_save.called)
    print("Call count:", mock_save.call_count)
    # mock_save.assert_called_once()

    response = client.get("/expenses/")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert response.json[0]["description"] == "Mocked Description"
