import argparse
import time


from api import api_calls
from mikrotik import Mikrotik
from ipaddress import IPv4Address

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS]",
        description="Start mikrotik profile"
    )
    parser.add_argument(
        "--api",
        help="the api to be called",
        required=True,
        choices=["interface_print", "interface_get"]
    )
            
    parser.add_argument("-t", "--time", help="the time between two api calls", type=int, default=5)
    return parser

def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()

    query = api_calls(args.api)
    mk_args = {
        "host_ip": IPv4Address("192.168.0.14"),
        "username": "admin",
        "password": ""
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
