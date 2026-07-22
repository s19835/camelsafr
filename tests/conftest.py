import io
import pytest
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd


@pytest.fixture
def fake_table():
    """Minimal pyarrow Table mimicking a static Parquet file."""
    return pa.table({
        "Basin_ID": ["L1_001", "L1_002"],
        "p_mean":   [1200.5,   800.3],
        "area_km2": [5000.0,   3200.0],
        "lat":      [-4.5,     10.2],
        "lng":      [23.1,     30.4],
        "country":  ["DRC",    "Ethiopia"],
        "country_iso3": ["COD", "ETH"],
    })


@pytest.fixture
def fake_df(fake_table):
    return fake_table.to_pandas()


@pytest.fixture
def annual_table():
    """Timeseries Parquet fixture (annual freq)."""
    return pa.table({
        "Basin_ID": ["L1_001", "L1_001", "L1_002"],
        "Year":     [2000,     2001,     2000],
        "p_arc":    [1200.5,   1150.0,   800.3],
        "pet_mean": [1500.0,   1480.0,   1200.0],
    })
