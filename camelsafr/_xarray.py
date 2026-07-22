from __future__ import annotations
import pandas as pd


def to_xarray(df: pd.DataFrame, freq: str):
    """Convert a timeseries DataFrame to an xarray Dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain Basin_ID and either Year (annual) or Date (daily/monthly).
    freq : str
        One of 'daily', 'monthly', 'annual' — determines the time index column.

    Returns
    -------
    xr.Dataset
    """
    try:
        import xarray as xr  # noqa: F401
    except (ImportError, TypeError):
        raise ImportError(
            "xarray is required for as_xarray=True. "
            "Install it with: pip install camelsafr[xarray]"
        )

    time_col = "Year" if freq == "annual" else "Date"
    if time_col not in df.columns:
        raise ValueError(
            f"Expected column '{time_col}' for freq='{freq}', "
            f"got columns: {list(df.columns)}"
        )

    return df.set_index(["Basin_ID", time_col]).to_xarray()
