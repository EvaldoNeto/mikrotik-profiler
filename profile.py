import argparse
import time


from api import api_calls
from mikrotik import Mikrotik
from ipaddress import IPv4Address

from influx import save_data

from load_config import load_influx_vars, load_mikrotik_vars


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS]",
        description="Start mikrotik profile"
    )
    parser.add_argument(
        "--api",
        help="the api to be called",
        required=True,
        choices=["interface_print", "interface_get", "interface_ethernet_print"]
    )
            
    parser.add_argument("-t", "--time", help="the time between two api calls", type=float, default=5)
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    query = api_calls(args.api)

    mk_vars = load_mikrotik_vars()
    username = mk_vars["USERNAME"]
    password = mk_vars["PASSWORD"]
    host = mk_vars["HOST"]
    timeout = mk_vars["TIMEOUT"]
    port = mk_vars["API_PORT"]
    mk_args = {
        "host_ip": IPv4Address(host),
        "username": username,
        "password": password,
        "apiPort": port,
        "timeout": timeout
    }
    mk = Mikrotik(**mk_args)
    try:
        mk.set_query(query)
        mk.api_connect()
    except Exception as err:
        print(err)
        exit(0)
    
    while True:
        x = mk.exec_query()
        print(x)
        time.sleep(args.time)

if __name__ == "__main__":
    main()
