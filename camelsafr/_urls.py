CDN_BASE = "https://d3w56ds7wplvdd.cloudfront.net/parquet"

STATIC_CATEGORIES = [
    "climate", "hydrology", "location", "geology", "soil", "landcover"
]

FREQ_TO_FILE = {
    "daily":   "climate_daily",
    "monthly": "climate_monthly",
    "annual":  "climate_annual",
}

VALID_LEVELS = {"L1", "L2", "L3", "L4"}


def static_url(level: str, category: str) -> str:
    return f"{CDN_BASE}/{level}_{category}_static.parquet"


def timeseries_url(level: str, freq: str) -> str:
    return f"{CDN_BASE}/{level}_{FREQ_TO_FILE[freq]}.parquet"
