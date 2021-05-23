import pytest
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
    sensor = ds18b20.DS18B20(input_file)

    assert sensor.poke() == 22.125
