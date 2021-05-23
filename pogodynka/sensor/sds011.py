import serial


class SDS011:
    """
    SDS011 sensor is publishing packets at 1Hz rate using following protocol:

        Byte Name           Content
        0    Message header AA
        1    Commander No.  C0
        2    DATA 1         PM2.5 Low byte
        3    DATA 2         PM2.5 High byte
        4    DATA 3         PM10 Low byte
        5    DATA 4         PM10 High byte
        6    DATA 5         ID byte 1
        7    DATA 6         ID byte 2
        8    Check-sum      Check-sum
        9    Message tail   AB

    Message integrity validation may be done with checksum:

        Check-sum = DATA1 + DATA2 + ... + DATA6

    Value of PM2.5/PM10 in μg/m3 may be calculated using formula:

        ((PM2.5 high byte * 256) + PM2.5 low byte) / 10
        ((PM10  high byte * 256) + PM10  low byte) / 10
    """

    DATA_PACKET_SIZE = 10
    MEASUREMENT_PM25_TYPE = "PM2.5"
    MEASUREMENT_PM10_TYPE = "PM10"

    def __init__(self, device_path):
        self.device_path = device_path

    def poke_25(self):
        data = self.read_pm_data()
        return int.from_bytes(b"".join(data[2:4]), byteorder="little") / 10

    def poke_10(self):
        data = self.read_pm_data()
        return int.from_bytes(b"".join(data[4:6]), byteorder="little") / 10

    def poke_25_with_time(self, time):
        return sensor.Measurement(
            time=time,
            type=self.MEASUREMENT_PM25_TYPE,
            value=self.poke_25(),
        )

    def poke_10_with_time(self, time):
        return sensor.Measurement(
            time=time,
            type=self.MEASUREMENT_PM10_TYPE,
            value=self.poke_10(),
        )
