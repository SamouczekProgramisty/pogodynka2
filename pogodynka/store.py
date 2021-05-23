import json
import datetime
from pogodynka import sensor


class StoreError(Exception):
    pass


GBQ_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def stream_to_gbq(client, scoped_table, measurements):
    rows_to_insert = []
    for measurement in measurements:
        row = {
            "time": measurement.time.strftime(GBQ_TIMESTAMP_FORMAT),
            "type": measurement.type,
            "value": measurement.value,
        }
        rows_to_insert.append(row)

    errors = client.insert_rows_json(scoped_table, rows_to_insert)
    if errors != []:
        raise StoreError(errors)
