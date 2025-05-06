from src.s3_handler import save_expense_to_s3, load_expenses_from_s3


def test_load_expenses_from_s3() -> None:
    """ Test the load_expenses_from_s3 function. """
    # Load expenses from S3
    df = load_expenses_from_s3()

    # Check if the DataFrame is not empty
    assert not df.empty

    # Check if the DataFrame has the expected columns
    expected_columns = [
        "date", "category", "amount",
        "payment_method", "description"
    ]
    assert all(col in df.columns for col in expected_columns)
    assert len(df.columns) == len(expected_columns)
    # Check if the DataFrame has the expected number of rows
    assert df.shape[0] > 0
    # Check if the DataFrame has the expected number of columns
    assert df.shape[1] == len(expected_columns)
    # Check if the DataFrame has the expected data types
    assert df["date"].dtype == "object"
    assert df["category"].dtype == "object"
    assert df["amount"].dtype == "object"  # "float64"
    assert df["payment_method"].dtype == "object"
    assert df["description"].dtype == "object"


def test_save_expense_to_s3() -> None:
    """ Test the save_expense_to_s3 function. """
    # Create a mock expense DataFrame
    mock_expense = {
        "date": "2023-10-01",
        "category": "Food",
        "amount": 50.0,
        "payment_method": "Credit Card",
        "description": "Groceries"
    }

    # Call the save_expense_to_s3 function
    save_expense_to_s3(mock_expense)

    # Load expenses from S3
    df = load_expenses_from_s3()

    # Check if the DataFrame is not empty
    assert not df.empty

    # Check if the DataFrame has the expected data
    assert df.iloc[-1]["date"] == "2023-10-01"
    assert df.iloc[-1]["category"] == "Food"
    assert df.iloc[-1]["amount"] == "50.0"
    assert df.iloc[-1]["payment_method"] == "Credit Card"
    assert df.iloc[-1]["description"] == "Groceries"
    # Check if the DataFrame has the expected number of rows
    assert df.shape[0] > 0
    # Check if the DataFrame has the expected number of columns
    assert df.shape[1] == 5
    # Check if the DataFrame has the expected columns
    expected_columns = [
        "date", "category", "amount",
        "payment_method", "description"
    ]
    assert all(col in df.columns for col in expected_columns)
    assert len(df.columns) == len(expected_columns)

    # Check if the DataFrame has the expected data types
    assert df["date"].dtype == "object"
    assert df["category"].dtype == "object"
    assert df["amount"].dtype == "object"  # "float64"
    assert df["payment_method"].dtype == "object"
    assert df["description"].dtype == "object"
