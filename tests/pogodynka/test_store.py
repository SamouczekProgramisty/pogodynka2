import pytest
import datetime
from pogodynka import sensor, store


@pytest.fixture
def measurements():
    return [
        sensor.Measurement(
            time=datetime.datetime.utcnow(),
            pm25=2.1,
            pm10=3.2,
            temperature=12.125,
        ),
        sensor.Measurement(
            time=datetime.datetime.utcnow(),
            pm25=3.1,
            pm10=4.2,
            temperature=12.125,
        ),
    ]


def test_cache(tmpdir, measurements):
    cache_path = str(tmpdir / "cache.bin")

    cache = store.Cache(cache_path)
    cache.dump(measurements)

    assert cache.load() == measurements


def test_load_empty_cache(tmpdir):
    cache = store.Cache(str(tmpdir / "mising.bin"))

    assert cache.load() == []


def test_clear_cache(tmpdir, measurements):
    cache = store.Cache(str(tmpdir / "cache.bin"))

    cache.dump(measurements)
    cache.clear()

    assert cache.load() == []
