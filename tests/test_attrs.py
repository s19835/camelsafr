import pytest
import pandas as pd
import camelsafr as ca

# monkeypatch target: "camelsafr.read_parquet" — patching the name bound in __init__
_PATCH = "camelsafr.read_parquet"

FAKE_DF = pd.DataFrame({
    "Basin_ID": ["L1_001", "L1_002"],
    "p_mean":   [1200.5,   800.3],
})

FAKE_LOC_DF = pd.DataFrame({
    "Basin_ID":    ["L1_001", "L1_002"],
    "lat":         [-4.5,     10.2],
    "lng":         [23.1,     30.4],
    "country":     ["DRC",    "Ethiopia"],
    "country_iso3":["COD",    "ETH"],
})


def test_attrs_returns_dataframe(monkeypatch):
    monkeypatch.setattr(_PATCH, lambda url, **kw: FAKE_DF)
    df = ca.attrs(level="L1")
    assert isinstance(df, pd.DataFrame)
    assert "Basin_ID" in df.columns


def test_attrs_calls_all_six_categories(monkeypatch):
    urls_called = []
    def fake_read(url, **kw):
        urls_called.append(url)
        return FAKE_DF.copy()
    monkeypatch.setattr(_PATCH, fake_read)
    ca.attrs(level="L2")
    categories = [u.split("_")[1] for u in urls_called]
    assert set(categories) == {"climate", "hydrology", "location", "geology", "soil", "landcover"}


def test_attrs_merges_on_basin_id(monkeypatch):
    calls = [0]
    def fake_read(url, **kw):
        calls[0] += 1
        extra_col = f"col_{calls[0]}"
        return pd.DataFrame({"Basin_ID": ["L1_001"], extra_col: [calls[0]]})
    monkeypatch.setattr(_PATCH, fake_read)
    df = ca.attrs(level="L1")
    assert "Basin_ID" in df.columns
    assert df.shape[0] == 1  # one basin across all merges


def test_attrs_invalid_level():
    with pytest.raises(ValueError, match="level must be one of"):
        ca.attrs(level="L99")


def test_attrs_passes_cache(monkeypatch):
    cache_vals = []
    def fake_read(url, **kw):
        cache_vals.append(kw.get("cache"))
        return FAKE_DF.copy()
    monkeypatch.setattr(_PATCH, fake_read)
    ca.attrs(level="L1", cache=True)
    assert all(v is True for v in cache_vals)


def test_basins_returns_metadata_columns(monkeypatch):
    monkeypatch.setattr(_PATCH, lambda url, **kw: FAKE_LOC_DF)
    df = ca.basins(level="L1")
    assert list(df.columns) == ["Basin_ID", "lat", "lng", "country", "country_iso3"]


def test_basins_uses_location_static(monkeypatch):
    urls = []
    monkeypatch.setattr(_PATCH, lambda url, **kw: (urls.append(url), FAKE_LOC_DF)[1])
    ca.basins(level="L3")
    assert any("location_static" in u for u in urls)


def test_basins_invalid_level():
    with pytest.raises(ValueError, match="level must be one of"):
        ca.basins(level="L5")
