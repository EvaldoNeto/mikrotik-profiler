"""
Here we just call the mikrotik profile api and send the data retrieved to
the database
"""

from librouteros import connect
from librouteros.login import plain

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from load_config import load_influx_vars, load_mikrotik_vars

import socket
import time

def mk_connect():
    """
    simple function to connect to a mikrotik and return a timeout error
    """
    mk_vars = load_mikrotik_vars()
    username = mk_vars["USERNAME"]
    password = mk_vars["PASSWORD"]
    host = mk_vars["HOST"]
    timeout = mk_vars["TIMEOUT"]
    port = mk_vars["API_PORT"]
    try:
        api = connect(
            username=username,
            password=password,
            host=host,
            login_method=plain,
            timeout=timeout,
            port=port
        )
        return api
    except socket.timeout as err:
        # when the api timeouts it raises a socket.timeout error, here we re-raise it to be used afterwards
        raise socket.timeout("mikrotik api timeout")
    except Exception as err:
        print("standard exception")
        print(err)

def save_data(data):
    name = data['name']
    usage = float(data['usage'])
    section = data['.section']

    influx_vars = load_influx_vars()
    bucket = influx_vars["INFLUX_BUCKET_NAME"]
    token = influx_vars["INFLUX_TOKEN"]
    org = influx_vars["INFLUX_ORG"]

    client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)

    write_api = client.write_api(write_options=SYNCHRONOUS)
    # p = Point("mikrotik_profile").tag("name", name).tag('section', section).field("usage2", usage)
    p = Point("mikrotik_profile").tag("name", name).field("usage", usage)

    write_api.write(bucket=bucket, record=p)

if __name__ == "__main__":
    try:
        api = mk_connect()
    except socket.timeout as err:
        # getting the timeout error that is re-raised by the mk_timeout_connect() function
        print(err)
    except Exception as err:
        print(err)


    query = api("/tool/profile")
    files = []
    tic = time.perf_counter()
    for row in query:
        print(row)
        save_data(row)
        toc = time.perf_counter()
        #if toc - tic > 20:
        #    break
        #files.append(row)


# https://github.com/influxdata/influxdb-client-python