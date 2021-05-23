import datetime
import json


class Measurement:
    def __init__(self, time, type, value):
        self.time = time
        self.type = type
        self.value = value
