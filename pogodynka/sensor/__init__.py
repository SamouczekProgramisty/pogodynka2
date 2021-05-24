import dataclasses
import datetime


@dataclasses.dataclass
class Measurement:
    time: datetime.datetime
    pm25: float
    pm10: float
    temperature: float
