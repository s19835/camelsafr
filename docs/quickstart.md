# Quickstart

## Install

```bash
pip install camelsafr
```

For xarray output support:

```bash
pip install camelsafr[xarray]
```

## First steps

```python
import camelsafr as ca

# Print a dataset overview
ca.info()
```

Output:
```
CAMELS-Afr dataset summary
  Levels:
    L1: 37 basins
    L2: 238 basins
    L3: 3,533 basins
    L4: 12,129 basins
  Static attributes: 216 per basin (climate, hydrology, location, geology, soil, land cover)
  Timeseries: daily / monthly / annual (1980–2024)
  Precipitation products: ARC, CHIRPS, IMERG, MSWEP
```

## Load static attributes

```python
df = ca.attrs(level='L1')
print(df.shape)       # (37, 217)  — 37 basins, Basin_ID + 216 attrs
print(df.columns[:5].tolist())
```

## Query timeseries

```python
ts = ca.timeseries(
    level='L1',
    basin_ids=['L1_001', 'L1_002'],
    freq='annual',
    variables=['p_arc', 'p_chirps', 'pet_mean'],
)
print(ts.head())
```

## Basin metadata

```python
meta = ca.basins(level='L2')
print(meta.head())
# Basin_ID  lat     lng    country  country_iso3
```

## Cache data locally

```python
# First call downloads to ~/.cache/camelsafr/
df = ca.attrs(level='L3', cache=True)

# Subsequent calls use the local file — no network request
df = ca.attrs(level='L3', cache=True)

# Clear the cache
ca.clear_cache(level='L3')
```
