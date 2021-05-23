from unittest import mock
import datetime
import pytest

from pogodynka import sensor
from pogodynka.sensor import sds011


@pytest.fixture
def port_mock():
    port_mock = mock.MagicMock()
    port_mock.read.return_value = b"\xaa\xc0\x1c\x001\x00\x0b\x141\xab"

    return port_mock


def test_pm25(port_mock):
    pm_sensor = sds011.SDS011(port_mock)

    poke_time = datetime.datetime(2021, 5, 23, 19, 45, 35, tzinfo=datetime.timezone.utc)

    assert pm_sensor.poke_25(poke_time) == sensor.Measurement(
        time=poke_time,
        value=2.8,
        type="PM2.5",
    )


def test_pm10(port_mock):
    pm_sensor = sds011.SDS011(port_mock)

    poke_time = datetime.datetime(2021, 5, 23, 19, 45, 35, tzinfo=datetime.timezone.utc)

    assert pm_sensor.poke_10(poke_time) == sensor.Measurement(
        time=poke_time,
        value=4.9,
        type="PM10",
    )
