"""camelsafr — Python client for the CAMELS-Afr hydrological database."""
from __future__ import annotations

from typing import Optional

import pandas as pd

from camelsafr._urls import (
    STATIC_CATEGORIES, VALID_LEVELS, FREQ_TO_FILE,
    static_url, timeseries_url,
)
import camelsafr._io as _io

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
            frames.append(_io.read_parquet(url, cache=cache))
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
    df = _io.read_parquet(url, cache=cache)
    keep = [c for c in ["Basin_ID", "lat", "lng", "country", "country_iso3"]
            if c in df.columns]
    return df[keep].reset_index(drop=True)


def timeseries(
    level: str = "L1",
    *,
    basin_ids: Optional[list] = None,
    freq: str = "annual",
    variables: Optional[list] = None,
    cache: bool = False,
    as_xarray: bool = False,
) -> pd.DataFrame:
    """Return climate timeseries for the given level and frequency."""
    _validate_level(level)
    if freq not in FREQ_TO_FILE:
        raise ValueError(f"freq must be one of {list(FREQ_TO_FILE)}, got {freq!r}")

    filters = [("Basin_ID", "in", basin_ids)] if basin_ids is not None else None

    columns: Optional[list] = None
    if variables is not None:
        time_col = "Year" if freq == "annual" else "Date"
        columns = list({"Basin_ID", time_col, *variables})

    url = timeseries_url(level, freq)
    df = _io.read_parquet(url, cache=cache, filters=filters, columns=columns)

    if as_xarray:
        from camelsafr._xarray import to_xarray
        return to_xarray(df, freq)
    return df


def info() -> None:
    raise NotImplementedError


def clear_cache(level: Optional[str] = None) -> None:
    raise NotImplementedError
