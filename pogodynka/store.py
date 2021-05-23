from google.cloud import bigquery


def stream_to_gbq(client, measurements):
    for measurement in measurements:
        print(client)
