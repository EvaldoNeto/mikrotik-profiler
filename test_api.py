from librouteros import connect
from librouteros.login import plain
from librouteros.query import Key
from librouteros.exceptions import TrapError

import time
import socket


def mk_connect():
    """
    simple function to connect to a mikrotik and return a timeout error
    """
    method = plain
    try:
        api = connect(username="admin", password="", host="192.168.0.14", login_method=plain, timeout=10, port=8728)
        return api
    except socket.timeout as err:
        # when the api timeouts it raises a socket.timeout error, here we re-raise it to be used afterwards
        raise socket.timeout("mikrotik api timeout")
    except Exception as err:
        print("standard exception")
        print(err)
        raise Exception("mopa")

def api_call():
    try:
        api = mk_connect()
    except socket.timeout as err:
        # getting the timeout error that is re-raised by the mk_timeout_connect() function
        print(err)
        api = None
    except Exception as err:
        api = None
        print(err)



    if api is None:
        return None

    query = api("/interface/print")
    files = []
    tic = time.perf_counter()
    for row in query:
        print(row)
    toc = time.perf_counter()
    print(f"time elapsed: {toc -tic}")
    return 1

if __name__ == "__main__":
    while True:
        time.sleep(1)
        api_call()
