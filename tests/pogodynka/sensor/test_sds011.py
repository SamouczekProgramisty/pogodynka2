from unittest import mock
import pytest

from pogodynka.sensor import sds011


@pytest.fixture
def port_mock():
    port_mock = mock.MagicMock()
    port_mock.read.return_value = b"\xaa\xc0\x1c\x001\x00\x0b\x141\xab"

    return port_mock


def test_pm25(port_mock):
    pm_sensor = sds011.SDS011(port_mock)

    assert pm_sensor.poke_25() == pytest.approx(2.8)


def test_pm10(port_mock):
    pm_sensor = sds011.SDS011(port_mock)

    assert pm_sensor.poke_10() == pytest.approx(4.9)
