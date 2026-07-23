# API Reference

## `ca.attrs(level, *, cache=False)`

Return all static attributes for every basin at the given level.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `level` | `str` | `'L1'` | One of `'L1'`, `'L2'`, `'L3'`, `'L4'` |
| `cache` | `bool` | `False` | Cache Parquet locally on first call |

**Returns:** `pd.DataFrame` — one row per basin; columns = `Basin_ID` + 216 static attributes.

**Example:**
```python
df = ca.attrs(level='L3')
```

---

## `ca.timeseries(level, *, basin_ids=None, freq='annual', variables=None, cache=False, as_xarray=False)`

Return climate timeseries for the given level and frequency.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `level` | `str` | `'L1'` | One of `'L1'`, `'L2'`, `'L3'`, `'L4'` |
| `basin_ids` | `list[str]` or `None` | `None` | Filter to specific basins; `None` returns all |
| `freq` | `str` | `'annual'` | One of `'daily'`, `'monthly'`, `'annual'` |
| `variables` | `list[str]` or `None` | `None` | Columns to return; `None` returns all |
| `cache` | `bool` | `False` | Cache Parquet locally on first call |
| `as_xarray` | `bool` | `False` | Return `xr.Dataset` instead of `pd.DataFrame` |

**Returns:** `pd.DataFrame` or `xr.Dataset`.

**Example:**
```python
ts = ca.timeseries(level='L2', basin_ids=['L2_001'], freq='annual',
                   variables=['p_arc', 'pet_mean'])
```

---

## `ca.basins(level, *, cache=False)`

Return basin metadata.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `level` | `str` | `'L1'` | One of `'L1'`, `'L2'`, `'L3'`, `'L4'` |
| `cache` | `bool` | `False` | Cache Parquet locally on first call |

**Returns:** `pd.DataFrame` with columns `Basin_ID`, `lat`, `lng`, `country`, `country_iso3`.

---

## `ca.info()`

Print a summary of dataset levels, basin counts, attribute groups, and timeseries coverage to stdout.

---

## `ca.clear_cache(level=None)`

Remove cached Parquet files.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `level` | `str` or `None` | `None` | Level to clear; `None` wipes all of `~/.cache/camelsafr/` |
