import serial
import datetime
import argparse

from google.cloud import bigquery

from pogodynka import store, sensor
from pogodynka.sensor import ds18b20, sds011


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
    temperature_sensor = ds18b20.DS18B20(args.temperature_sensor_path)

    cache = store.Cache(args.cache_path)

    measurements = cache.load()
    measurements.append(
        sensor.Measurement(
            time=datetime.datetime.utcnow(),
            pm25=pm_sensor.poke_25(),
            pm10=pm_sensor.poke_10(),
            temperature=temperature_sensor.poke(),
        ),
    )

    gbq_client = bigquery.Client()

    try:
        store.stream_to_gbq(gbq_client, args.destination_table, measurements)
        cache.clear()
    except store.StoreError:
        cache.dump(measurements)
        raise


if __name__ == "__main__":
    main()
