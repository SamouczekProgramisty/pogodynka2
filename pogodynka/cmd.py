import serial
import datetime
import argparse

from google.cloud import bigquery

from pogodynka.sensor import ds18b20, sds011
from pogodynka import store


SENSOR_TEMPERATURE = "temperature"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--temperature-sensor-path", required=True)
    parser.add_argument("--pm-sensor-device", required=True)
    parser.add_argument("--cache-path", default="/tmp/pogodynka.bin")
    parser.add_argument(
        "--destination-table", default="sp-pogodynka.sensor.measurement"
    )

    args = parser.parse_args()

    pm_port = serial.Serial(args.pm_sensor_device)
    pm_sensor = sds011.SDS011(pm_port)
    temperature_sensor = sds011.SDS011(args.pm_sensor_device)
    measurement_time = datetime.datetime.utcnow()

    cache = store.Cache(args.cache_path)

    measurements = cache.load()
    measurements.extend(
        [
            pm_sensor.poke_25(measurement_time),
            pm_sensor.poke_10(measurement_time),
            temperature_sensor.poke(measurement_time),
        ]
    )

    gbq_client = bigquery.Client()

    try:
        store.stream_to_gbq(gbq_client, args.destination_table, measurements)
    except store.StoreError:
        cache.dump(measurements)
        raise


if __name__ == "__main__":
    main()
