import os
import sys
import shutil
import pandas as pd

from src.db import save_expense, load_expenses


def setup_temp_csv_path(filename: str = "expenses_test.csv") -> str:
    """Set up and return a temporary CSV path, and mock the DATA_PATH."""
    temp_dir = os.path.join("data", "tmp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_csv_path = os.path.join(temp_dir, filename)
    sys.modules["src.db"].DATA_PATH = str(temp_csv_path)
    return temp_csv_path


def test_save_expense() -> None:
    """Test that save_expense correctly writes a single entry to CSV."""
    temp_csv_path = setup_temp_csv_path()

    mock_expense = {
        "date": "2023-10-01",
        "category": "Food",
        "amount": 50.0,
        "payment_method": "Credit Card",
        "description": "Groceries"
    }

    try:
        df_mock = pd.DataFrame([mock_expense])
        save_expense(df_mock)

        assert os.path.exists(temp_csv_path)

        df = load_expenses()
        assert not df.empty
        assert df.shape[0] == 1
        for key, value in mock_expense.items():
            assert df.iloc[0][key] == value
    finally:
        shutil.rmtree(os.path.dirname(temp_csv_path))


def test_load_expenses() -> None:
    """Test that load_expenses correctly loads a populated CSV file."""
    temp_csv_path = setup_temp_csv_path()

    mock_data = {
        "date": ["2023-10-01", "2023-10-02"],
        "category": ["Food", "Transport"],
        "amount": [50.0, 20.0],
        "payment_method": ["Credit Card", "Cash"],
        "description": ["Groceries", "Bus Ticket"]
    }

    try:
        df = pd.DataFrame(mock_data)
        df.to_csv(temp_csv_path, index=False)

        loaded_df = load_expenses()
        assert loaded_df.shape == (2, 5)
        for i in range(2):
            for col in df.columns:
                assert loaded_df.iloc[i][col] == mock_data[col][i]
    finally:
        shutil.rmtree(os.path.dirname(temp_csv_path))


def test_load_expenses_empty() -> None:
    """
    Test that load_expenses returns an empty
    DataFrame if the CSV file doesn't exist.
    """
    temp_csv_path = setup_temp_csv_path()

    try:
        loaded_df = load_expenses()

        assert loaded_df.empty
        assert list(loaded_df.columns) == ["date", "category", "amount",
                                           "payment_method", "description"
                                           ]
        assert loaded_df.shape == (0, 5)
        assert all(col in loaded_df.columns for col in ["date",
                                                        "category",
                                                        "amount",
                                                        "payment_method",
                                                        "description"
                                                        ])
        assert all(str(loaded_df[col].dtype) == "object"
                   for col in loaded_df.columns)
    finally:
        # Clean up the temp directory
        shutil.rmtree(os.path.dirname(temp_csv_path))


def test_save_expense_appends_to_existing_file() -> None:
    """Test that save_expense appends a new expense instead of overwriting."""
    # Setup temp path and mock DATA_PATH
    temp_dir = os.path.join("data", "tmp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_csv_path = os.path.join(temp_dir, "expenses_test.csv")

    import sys
    sys.modules["src.db"].DATA_PATH = str(temp_csv_path)

    # First mock expense
    df1 = pd.DataFrame([{
        "date": "2023-10-01",
        "category": "Food",
        "amount": 30.0,
        "payment_method": "Cash",
        "description": "Lunch"
    }])

    # Second mock expense
    df2 = pd.DataFrame([{
        "date": "2023-10-02",
        "category": "Transport",
        "amount": 10.0,
        "payment_method": "Credit Card",
        "description": "Metro Ticket"
    }])

    # Save both
    save_expense(df1)
    save_expense(df2)

    # Load and test
    df = load_expenses()
    assert df.shape[0] == 2
    assert df.iloc[0]["description"] == "Lunch"
    assert df.iloc[1]["description"] == "Metro Ticket"

    # Clean up
    shutil.rmtree(temp_dir)
