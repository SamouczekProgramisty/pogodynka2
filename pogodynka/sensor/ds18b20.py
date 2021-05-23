from pogodynka import sensor


class DS18B20:

    MEASUREMENT_TYPE = "temperature"

    def __init__(self, file_path):
        self.file_path = file_path

    def raw_poke(self):
        with open(self.file_path) as input_file:
            lines = input_file.readlines()
            assert len(lines) == 2
            _, temperature = lines[1].split("=")
            temperature = int(temperature)
            return temperature / 1000

    def poke(self, time):
        return sensor.Measurement(
            time=time,
            type=self.MEASUREMENT_TYPE,
            value=self.raw_poke(),
        )
