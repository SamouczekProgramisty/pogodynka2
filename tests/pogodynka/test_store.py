import datetime
from pogodynka import sensor, store


def test_cache(tmpdir):
    cache_path = str(tmpdir / "cache.bin")

    cache = store.Cache(cache_path)

    measurements = [
        sensor.Measurement(
            time=datetime.datetime.utcnow(),
            type="pm10",
            value=12.125,
        ),
        sensor.Measurement(
            time=datetime.datetime.utcnow(),
            type="temperature",
            value=12.125,
        ),
        sensor.Measurement(
            time=datetime.datetime.utcnow(),
            type="pm2.5",
            value=12.125,
        ),
    ]

    cache.dump(measurements)

    assert cache.load() == measurements


def test_load_empty_cache(tmpdir):
    cache = store.Cache(str(tmpdir / "mising.bin"))

    assert cache.load() == []
