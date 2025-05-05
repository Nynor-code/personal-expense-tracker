# tests/test_app.py

import json
from src.main import app


def test_add_and_get_expense():
    test_payload = {
        "date": "2025-05-05",
        "category": "Test",
        "amount": 42.0,
        "payment_method": "Credit Card",
        "description": "Test expense"
    }

    with app.test_client() as client:
        # POST new expense
        res = client.post("/add_expense/", data=json.dumps(test_payload),
                          content_type='application/json')
        assert res.status_code == 200
        assert res.get_json()["status"] == "Expense Saved"

        # GET expenses
        res = client.get("/expenses/")
        assert res.status_code == 200
        expenses = res.get_json()
        assert any(exp["category"] == "Test" for exp in expenses)
