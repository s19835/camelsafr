import os
import pytest
import pyarrow as pa
import pandas as pd
from unittest.mock import patch, MagicMock
from camelsafr._io import read_parquet, cache_path, _cache_dir


def test_cache_dir_default(tmp_path, monkeypatch):
    monkeypatch.delenv("XDG_CACHE_HOME", raising=False)
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    assert _cache_dir() == tmp_path / ".cache" / "camelsafr"


def test_cache_dir_xdg(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg"))
    assert _cache_dir() == tmp_path / "xdg" / "camelsafr"


def test_cache_path(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    p = cache_path("L3", "L3_climate_annual.parquet")
    assert p == tmp_path / "camelsafr" / "L3" / "L3_climate_annual.parquet"


def _mock_urlopen(fake_table):
    """Return a context-manager mock whose .read() yields fake parquet bytes."""
    import io
    import pyarrow.parquet as pq_mod
    buf = io.BytesIO()
    pq_mod.write_table(fake_table, buf)
    buf.seek(0)
    mock_resp = MagicMock()
    mock_resp.status = 200
    mock_resp.read.return_value = buf.read()
    mock_resp.__enter__ = MagicMock(return_value=mock_resp)
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


def test_read_parquet_no_cache(fake_table, monkeypatch):
    mock_resp = _mock_urlopen(fake_table)
    with patch("urllib.request.urlopen", return_value=mock_resp):
        df = read_parquet("https://cdn.example.com/L1_climate_annual.parquet")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


def test_read_parquet_passes_filters(fake_table, monkeypatch):
    mock_resp = _mock_urlopen(fake_table)
    with patch("urllib.request.urlopen", return_value=mock_resp):
        with patch("camelsafr._io.pq.read_table", return_value=fake_table) as mock_read:
            read_parquet("https://cdn.example.com/L1_climate_annual.parquet",
                         filters=[("Basin_ID", "in", ["L1_001"])])
    # filters are passed to read_table after BytesIO download
    mock_read.assert_called_once()
    _, kwargs = mock_read.call_args
    assert kwargs["filters"] == [("Basin_ID", "in", ["L1_001"])]


def test_read_parquet_cache_miss_downloads(fake_table, tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    url = "https://cdn.example.com/L1_climate_annual.parquet"
    downloaded = []

    def fake_download(u, dest):
        downloaded.append(u)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b"fake")

    with patch("camelsafr._io._download", side_effect=fake_download):
        with patch("camelsafr._io.pq.read_table", return_value=fake_table):
            df = read_parquet(url, cache=True)

    assert downloaded == [url]
    assert isinstance(df, pd.DataFrame)


def test_read_parquet_cache_hit_skips_download(fake_table, tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    url = "https://cdn.example.com/L1_climate_annual.parquet"
    local = tmp_path / "camelsafr" / "L1" / "L1_climate_annual.parquet"
    local.parent.mkdir(parents=True, exist_ok=True)
    local.write_bytes(b"cached")

    downloaded = []
    with patch("camelsafr._io._download", side_effect=lambda u, d: downloaded.append(u)):
        with patch("camelsafr._io.pq.read_table", return_value=fake_table):
            read_parquet(url, cache=True)

    assert downloaded == []  # no download on cache hit


def test_download_http_error(tmp_path, monkeypatch):
    from camelsafr._io import _download
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    url = "https://cdn.example.com/missing.parquet"
    dest = tmp_path / "camelsafr" / "L1" / "missing.parquet"

    mock_resp = MagicMock()
    mock_resp.status = 404
    mock_resp.__enter__ = MagicMock(return_value=mock_resp)
    mock_resp.__exit__ = MagicMock(return_value=False)

    with patch("urllib.request.urlopen", return_value=mock_resp):
        with pytest.raises(RuntimeError, match="HTTP 404"):
            _download(url, dest)
