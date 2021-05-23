import datetime
import pytest

from pogodynka import sensor
from pogodynka.sensor import ds18b20


@pytest.fixture
def input_file(tmpdir):
    input_path = str(tmpdir / "input_file")
    with open(input_path, "w") as input_file:
        input_file.write(
            """62 01 4b 46 7f ff 0e 10 03 : crc=03 YES
62 01 4b 46 7f ff 0e 10 03 t=22125"""
        )

    return input_path


def test_temperature_sensor(input_file):
    temperature_sensor = ds18b20.DS18B20(input_file)

    poke_time = datetime.datetime(2021, 5, 23, 19, 45, 35, tzinfo=datetime.timezone.utc)

    assert temperature_sensor.poke(poke_time) == sensor.Measurement(
        time=poke_time,
        value=22.125,
        type="temperature",
    )
