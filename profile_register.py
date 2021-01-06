"""
Here we just call the mikrotik profile api and send the data retrieved to
the database
"""

from librouteros import connect
from librouteros.login import plain
from librouteros.query import Key
from librouteros.exceptions import TrapError

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

import socket
import time

def mk_connect():
    """
    simple function to connect to a mikrotik and return a timeout error
    """
    method = plain
    try:
        api = connect(username="admin", password="", host="localhost", login_method=plain, timeout=10, port=28728)
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

    bucket = "biga_bucket"
    token = "kakaroto"
    client = InfluxDBClient(url="http://localhost:8086", token=token, org="biga")

    write_api = client.write_api(write_options=SYNCHRONOUS)
    # p = Point("mikrotik_profile").tag("name", name).tag('section', section).field("usage2", usage)
    p = Point("mikrotik_profile").tag("name", name).field("usage2", usage)

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