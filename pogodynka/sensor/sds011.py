from pogodynka import sensor


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

    HEADER = 0xAA
    TAIL = 0xAB

    def __init__(self, port):
        self.port = port

    def poke_25(self):
        data = self.read_bytes()
        # data[3] * 256 + data[2]
        return int.from_bytes(data[2:4], byteorder="little") / 10

    def poke_10(self):
        data = self.read_bytes()
        # data[5] * 256 + data[4]
        return int.from_bytes(data[4:6], byteorder="little") / 10

    def read_bytes(self):
        data = self.port.read(self.DATA_PACKET_SIZE)

        assert data[0] == self.HEADER
        assert data[9] == self.TAIL

        return data
