import pytest
from pathlib import Path
import camelsafr as ca


def test_clear_cache_all(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    cache = tmp_path / "camelsafr"
    (cache / "L1").mkdir(parents=True)
    (cache / "L1" / "L1_climate_annual.parquet").write_bytes(b"data")
    ca.clear_cache()
    assert not cache.exists()


def test_clear_cache_specific_level(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    cache = tmp_path / "camelsafr"
    (cache / "L1").mkdir(parents=True)
    (cache / "L2").mkdir(parents=True)
    (cache / "L1" / "file.parquet").write_bytes(b"L1")
    (cache / "L2" / "file.parquet").write_bytes(b"L2")
    ca.clear_cache(level="L1")
    assert not (cache / "L1").exists()
    assert (cache / "L2").exists()


def test_clear_cache_nonexistent_is_noop(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path))
    ca.clear_cache()  # should not raise


def test_clear_cache_invalid_level():
    with pytest.raises(ValueError, match="level must be one of"):
        ca.clear_cache(level="L99")


def test_info_prints_summary(capsys):
    ca.info()
    out = capsys.readouterr().out
    assert "CAMELS-Afr" in out
    assert "L1" in out
    assert "37" in out
    assert "12,129" in out or "12129" in out
