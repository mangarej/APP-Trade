# plotlyfinance/utils.py
import pandas as pd

def validate_data(data, required_cols):
    """Validate that the DataFrame contains required columns."""
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
    if not all(col in data.columns for col in required_cols):
        raise ValueError(f"DataFrame must contain columns: {required_cols}")