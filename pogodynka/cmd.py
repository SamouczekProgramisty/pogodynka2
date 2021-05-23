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
    parser.add_argument("--cache-directory")
    parser.add_argument("--sensor-location", default="")

    args = parser.parse_args()

    measurement_time = datetime.datetime.utcnow()

    pm_sensor = sds011.SDS011(args.pm_sensor_device)
    temperature_sensor = sds011.SDS011(args.pm_sensor_device)

    measurements = [
        lambda: {"value": pm_sensor.poke25()},
        lambda: {"value": pm_sensor.poke10()},
        lambda: {"value": temperature_sensor.poke()},
    ]

    gbq_client = bigquery.Client()

    store.stream_to_gbq(gbq_client, measurements)


if __name__ == "__main__":
    main()
