import pandas as pd

from src.ml_model import forecast_expenses


def test_forecast_expenses() -> None:
    """Test forecast_expenses() with dummy data."""
    data = {
        'date': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01'],
        'amount': [100, 150, 200, 250]
    }
    df = pd.DataFrame(data)
    result = forecast_expenses(df)

    assert isinstance(result, dict)
    assert all(isinstance(k, str) and k[:4].isdigit() for k in result)
    assert all(isinstance(v, float) for v in result.values())
    assert len(result) == 2


def test_forecast_with_empty_data() -> None:
    """Test forecast with empty data."""
    result = forecast_expenses([])
    assert "error" in result


def test_forecast_with_missing_columns() -> None:
    """Test forecast with missing columns."""
    df = pd.DataFrame({'date': ['2023-01-01']})  # No 'amount'
    result = forecast_expenses(df)
    assert "error" in result


def test_forecast_with_single_entry() -> None:
    """Test forecast with a single entry."""
    df = pd.DataFrame({'date': ['2023-01-01'], 'amount': [100]})
    result = forecast_expenses(df)
    assert "error" in result


def test_forecast_with_invalid_data() -> None:
    """Test forecast with invalid data types."""
    df = pd.DataFrame({'date': ['invalid-date', None],
                       'amount': ['NaN', None]}
                      )
    result = forecast_expenses(df)
    assert "error" in result


def test_forecast_keys_are_ordered_months() -> None:
    """Test if the forecasted keys are ordered by month."""
    df = pd.DataFrame({
        'date': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01'],
        'amount': [100, 150, 200, 250]
    })
    result = forecast_expenses(df)
    assert list(result.keys()) == sorted(result.keys())


def test_forecast_values_are_floats() -> None:
    """Test if the forecasted values are floats."""
    df = pd.DataFrame({
        'date': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01'],
        'amount': [100, 150, 200, 250]
    })
    result = forecast_expenses(df)
    assert all(isinstance(val, float) for val in result.values())
