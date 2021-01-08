from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


def save_data(data):
    name = data['name']
    usage = float(data['usage'])
    section = data['.section']

    bucket = "biga"
    token = "kakaroto"
    client = InfluxDBClient(url="http://localhost:8086", token=token, org="le_biga")

    write_api = client.write_api(write_options=SYNCHRONOUS)
    # p = Point("mikrotik_profile").tag("name", name).tag('section', section).field("usage2", usage)
    p = Point("mikrotik_profile").tag("name", name).field("usage", usage)

    write_api.write(bucket=bucket, record=p)