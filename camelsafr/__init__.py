"""camelsafr — Python client for the CAMELS-Afr hydrological database."""
from __future__ import annotations

from typing import Optional

import pandas as pd

from camelsafr._urls import (
    STATIC_CATEGORIES, VALID_LEVELS, FREQ_TO_FILE,
    static_url, timeseries_url,
)
from camelsafr._io import read_parquet, cache_path, _cache_dir

__version__ = "0.1.0"
__all__ = ["attrs", "timeseries", "basins", "info", "clear_cache"]


def _validate_level(level: str) -> None:
    if level not in VALID_LEVELS:
        raise ValueError(f"level must be one of {sorted(VALID_LEVELS)}, got {level!r}")


def attrs(level: str = "L1", *, cache: bool = False) -> pd.DataFrame:
    """Return all static attributes for every basin at the given level."""
    _validate_level(level)
    frames: list[pd.DataFrame] = []
    for cat in STATIC_CATEGORIES:
        url = static_url(level, cat)
        try:
            frames.append(read_parquet(url, cache=cache))
        except Exception:
            continue

    if not frames:
        raise RuntimeError(f"No static data found for level {level!r}")

    df = frames[0]
    for other in frames[1:]:
        df = df.merge(other, on="Basin_ID", how="outer", suffixes=("", "_dup"))
        df = df.drop(columns=[c for c in df.columns if c.endswith("_dup")])
    return df.reset_index(drop=True)


def basins(level: str = "L1", *, cache: bool = False) -> pd.DataFrame:
    """Return basin metadata (id, lat, lng, country) for the given level."""
    _validate_level(level)
    url = static_url(level, "location")
    df = read_parquet(url, cache=cache)
    keep = [c for c in ["Basin_ID", "lat", "lng", "country", "country_iso3"]
            if c in df.columns]
    return df[keep].reset_index(drop=True)


# Stubs — implemented in later tasks
def timeseries(level="L1", *, basin_ids=None, freq="annual",
               variables=None, cache=False, as_xarray=False):
    raise NotImplementedError


def info() -> None:
    raise NotImplementedError


def clear_cache(level: Optional[str] = None) -> None:
    raise NotImplementedError
