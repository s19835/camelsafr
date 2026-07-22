from camelsafr._urls import static_url, timeseries_url, STATIC_CATEGORIES, VALID_LEVELS

CDN = "https://d3w56ds7wplvdd.cloudfront.net/parquet"


def test_static_url():
    assert static_url("L1", "climate") == f"{CDN}/L1_climate_static.parquet"
    assert static_url("L3", "soil") == f"{CDN}/L3_soil_static.parquet"


def test_timeseries_url_annual():
    assert timeseries_url("L2", "annual") == f"{CDN}/L2_climate_annual.parquet"


def test_timeseries_url_daily():
    assert timeseries_url("L4", "daily") == f"{CDN}/L4_climate_daily.parquet"


def test_timeseries_url_monthly():
    assert timeseries_url("L1", "monthly") == f"{CDN}/L1_climate_monthly.parquet"


def test_static_categories_order():
    assert STATIC_CATEGORIES == [
        "climate", "hydrology", "location", "geology", "soil", "landcover"
    ]


def test_valid_levels():
    assert VALID_LEVELS == {"L1", "L2", "L3", "L4"}
