# tests/test_app.py
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_add_and_get_expense():
    payload = {"date": "2025-05-05", "category": "Test", "amount": 42.0}
    res = client.post("/add_expense/", json=payload)
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

    res = client.get("/expenses/")
    assert res.status_code == 200
    assert any(exp["category"] == "Test" for exp in res.json())

