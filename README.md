# camelsafr

[![PyPI](https://img.shields.io/pypi/v/camelsafr)](https://pypi.org/project/camelsafr/)
[![Docs](https://readthedocs.org/projects/camelsafr/badge/?version=latest)](https://camelsafr.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Python client for the **CAMELS-Afr** African basin hydrological database —
216 static attributes and 44 years of daily/monthly/annual timeseries for
15,937 basins across four spatial levels.

## Install

```bash
pip install camelsafr
# with xarray support:
pip install camelsafr[xarray]
```

## Quickstart

```python
import camelsafr as ca

ca.info()                              # print dataset summary
df = ca.attrs(level='L1')             # 37 basins × 216 attributes
ts = ca.timeseries(level='L1',
                   basin_ids=['L1_001'],
                   freq='annual')      # annual climate for one basin
```

## Documentation

Full docs at [camelsafr.readthedocs.io](https://camelsafr.readthedocs.io).

## Data

Data hosted on AWS CloudFront. No API key required.
Source: CGIAR Hydrology / IWMI. Citation: _[paper pending]_.
