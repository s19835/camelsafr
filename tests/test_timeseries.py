import pytest
import pandas as pd
import camelsafr as ca


ANNUAL_DF = pd.DataFrame({
    "Basin_ID": ["L1_001", "L1_001", "L1_002"],
    "Year":     [2000,     2001,     2000],
    "p_arc":    [1200.5,   1150.0,   800.3],
    "pet_mean": [1500.0,   1480.0,   1200.0],
})


def test_timeseries_returns_dataframe(monkeypatch):
    monkeypatch.setattr("camelsafr._io.read_parquet", lambda url, **kw: ANNUAL_DF)
    df = ca.timeseries(level="L1", freq="annual")
    assert isinstance(df, pd.DataFrame)
    assert "Basin_ID" in df.columns


def test_timeseries_uses_correct_url(monkeypatch):
    urls = []
    monkeypatch.setattr("camelsafr._io.read_parquet",
                        lambda url, **kw: (urls.append(url), ANNUAL_DF)[1])
    ca.timeseries(level="L2", freq="monthly")
    assert any("L2_climate_monthly" in u for u in urls)


def test_timeseries_passes_basin_id_filter(monkeypatch):
    kwargs_seen = {}
    def fake_read(url, **kw):
        kwargs_seen.update(kw)
        return ANNUAL_DF
    monkeypatch.setattr("camelsafr._io.read_parquet", fake_read)
    ca.timeseries(level="L1", basin_ids=["L1_001"], freq="annual")
    assert kwargs_seen["filters"] == [("Basin_ID", "in", ["L1_001"])]


def test_timeseries_no_filter_when_basin_ids_none(monkeypatch):
    kwargs_seen = {}
    def fake_read(url, **kw):
        kwargs_seen.update(kw)
        return ANNUAL_DF
    monkeypatch.setattr("camelsafr._io.read_parquet", fake_read)
    ca.timeseries(level="L1", freq="annual", basin_ids=None)
    assert kwargs_seen["filters"] is None


def test_timeseries_passes_columns_when_variables_given(monkeypatch):
    kwargs_seen = {}
    def fake_read(url, **kw):
        kwargs_seen.update(kw)
        return ANNUAL_DF[["Basin_ID", "Year", "p_arc"]]
    monkeypatch.setattr("camelsafr._io.read_parquet", fake_read)
    ca.timeseries(level="L1", freq="annual", variables=["p_arc"])
    assert set(kwargs_seen["columns"]) == {"Basin_ID", "Year", "p_arc"}


def test_timeseries_no_columns_when_variables_none(monkeypatch):
    kwargs_seen = {}
    def fake_read(url, **kw):
        kwargs_seen.update(kw)
        return ANNUAL_DF
    monkeypatch.setattr("camelsafr._io.read_parquet", fake_read)
    ca.timeseries(level="L1", freq="annual", variables=None)
    assert kwargs_seen["columns"] is None


def test_timeseries_invalid_level():
    with pytest.raises(ValueError, match="level must be one of"):
        ca.timeseries(level="L99")


def test_timeseries_invalid_freq():
    with pytest.raises(ValueError, match="freq must be one of"):
        ca.timeseries(level="L1", freq="decadal")


def test_timeseries_daily_uses_date_col_for_variables(monkeypatch):
    daily_df = pd.DataFrame({
        "Basin_ID": ["L1_001"],
        "Date": ["1980-01-01"],
        "p_mean_arc": [3.2],
    })
    kwargs_seen = {}
    def fake_read(url, **kw):
        kwargs_seen.update(kw)
        return daily_df[["Basin_ID", "Date", "p_mean_arc"]]
    monkeypatch.setattr("camelsafr._io.read_parquet", fake_read)
    ca.timeseries(level="L1", freq="daily", variables=["p_mean_arc"])
    assert "Date" in kwargs_seen["columns"]
