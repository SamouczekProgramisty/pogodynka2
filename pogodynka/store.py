import pickle
import json
import datetime

from os import path

from pogodynka import sensor

from google.cloud import exceptions


class StoreError(Exception):
    pass


GBQ_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def stream_to_gbq(client, scoped_table, measurements):
    rows_to_insert = []
    for measurement in measurements:
        row = {
            "time": measurement.time.strftime(GBQ_TIMESTAMP_FORMAT),
            "pm25": measurement.pm25,
            "pm10": measurement.pm10,
            "temperature": measurement.temperature,
        }
        rows_to_insert.append(row)

    try:
        errors = client.insert_rows_json(scoped_table, rows_to_insert)
    except exceptions.BadRequest as e:
        raise StoreError(e)

    if errors != []:
        raise StoreError(errors)


class Cache:
    def __init__(self, cache_path):
        self.cache_path = cache_path

    def load(self):
        if not path.isfile(self.cache_path):
            return []

        with open(self.cache_path, "rb") as cache_file:
            return pickle.load(cache_file)

    def dump(self, measurements):
        with open(self.cache_path, "wb") as cache_file:
            pickle.dump(measurements, cache_file)

    def clear(self):
        self.dump([])
