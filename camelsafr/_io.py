from __future__ import annotations

import os
import urllib.request
from pathlib import Path
from typing import Optional, List

import pyarrow.parquet as pq
import pandas as pd


def _cache_dir() -> Path:
    base = os.environ.get("XDG_CACHE_HOME")
    if base:
        return Path(base) / "camelsafr"
    return Path.home() / ".cache" / "camelsafr"


def cache_path(level: str, filename: str) -> Path:
    return _cache_dir() / level / filename


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as resp:
        if resp.status != 200:
            raise RuntimeError(f"HTTP {resp.status} fetching {url}")
        dest.write_bytes(resp.read())


def read_parquet(
    url: str,
    *,
    cache: bool = False,
    filters: Optional[list] = None,
    columns: Optional[List[str]] = None,
) -> pd.DataFrame:
    if cache:
        filename = url.rsplit("/", 1)[-1]
        level = filename.split("_")[0]
        local = cache_path(level, filename)
        if not local.exists():
            _download(url, local)
        source: str | Path = local
    else:
        import io as _io_mod
        with urllib.request.urlopen(url) as resp:
            if resp.status != 200:
                raise RuntimeError(f"HTTP {resp.status} fetching {url}")
            source = _io_mod.BytesIO(resp.read())

    table = pq.read_table(source, filters=filters, columns=columns)
    return table.to_pandas()
