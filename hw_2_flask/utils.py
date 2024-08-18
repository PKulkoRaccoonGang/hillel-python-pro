import pandas as pd


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the column names by stripping spaces and removing text within parentheses.

    Args:
        df (pd.DataFrame): The DataFrame with columns to clean.

    Returns:
        pd.DataFrame: The DataFrame with cleaned column names.
    """
    df.columns = df.columns.str.strip().str.replace(r'\s*\(.*\)\s*', '', regex=True)
    return df
  