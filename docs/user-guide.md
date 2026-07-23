# User Guide

## 1. Build an ML feature table

Load all L3 static attributes and use them as features for a machine learning model:

```python
import camelsafr as ca
import pandas as pd

# Load static attributes for all 3,533 L3 basins
df = ca.attrs(level='L3', cache=True)  # cache=True for offline reuse

# Drop non-numeric columns before feeding to a model
X = df.drop(columns=['Basin_ID']).select_dtypes(include='number')
print(X.shape)  # (3533, 215)
```

## 2. Query annual precipitation timeseries for selected basins

```python
import camelsafr as ca

# Annual timeseries for two specific basins
ts = ca.timeseries(
    level='L1',
    basin_ids=['L1_001', 'L1_015'],
    freq='annual',
    variables=['p_arc', 'p_chirps', 'p_imerg', 'p_mswep'],
)

# Plot precipitation products side-by-side
import matplotlib.pyplot as plt

for basin_id, grp in ts.groupby('Basin_ID'):
    fig, ax = plt.subplots()
    for col in ['p_arc', 'p_chirps', 'p_imerg', 'p_mswep']:
        ax.plot(grp['Year'], grp[col], label=col)
    ax.set_title(basin_id)
    ax.legend()
    plt.show()
```

## 3. Cache a level for offline use

```python
import camelsafr as ca

# First call: downloads to ~/.cache/camelsafr/L2/
df = ca.attrs(level='L2', cache=True)

# On a plane or cluster with no internet — works instantly from cache
df = ca.attrs(level='L2', cache=True)

# Free up disk space when done
ca.clear_cache(level='L2')
```

## 4. Load timeseries into xarray for multi-basin analysis

Requires `pip install camelsafr[xarray]`.

```python
import camelsafr as ca

ds = ca.timeseries(
    level='L1',
    freq='annual',
    variables=['p_arc', 'pet_mean'],
    as_xarray=True,
)
print(ds)
# <xarray.Dataset>
# Dimensions:   (Basin_ID: 37, Year: 44)
# Data variables:
#     p_arc     (Basin_ID, Year) float64 ...
#     pet_mean  (Basin_ID, Year) float64 ...

# Annual mean precipitation across all basins
ds['p_arc'].mean(dim='Basin_ID').plot()
```
