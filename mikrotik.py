"""
Here we have the mikrotik base class definition, we basically define
its basic attributes and connectors via api, ssh and ftp
"""

import socket

from ipaddress import IPv4Address

from pydantic import BaseModel
from typing import Any

from librouteros.login import plain, token
from librouteros import connect
from librouteros.exceptions import TrapError

from enum import Enum


class QueryException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'QueryException, {0} '.format(self.message)
        else:
            return 'QueryException has been raised'


class MKLoginError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'MKLoginError, {0} '.format(self.message)
        else:
            return 'MKLoginError has been raised'


class MkBool(str, Enum):
    """
    'Boolean' for the mikrotik configuration
    """
    no = 'no'
    yes = 'yes'


class LoginMethod(str, Enum):
    """
    """
    plain = 'plain'
    token = 'token'


class MkStatus(str, Enum):
    """
    Indicator of failure or success when calling the api
    """
    success = 'success'
    fail = 'fail'

class Mikrotik(BaseModel):
    """
    This class defines all data necessary for the connection
    on a mikrotik device
    """
    host_ip: IPv4Address
    password: str
    username: str = 'admin'
    timeout: float = 25
    apiPort: str = "8728"
    loginMethod: LoginMethod = LoginMethod.plain
    query = {}
    api: Any = None

    _loginMethods = {
        'plain': plain,
        'token': token
    }

    def set_query(self, query):
        """
        Set the query to be executed when the api connection is open
        query is a dict that contains the "query" and "args" keys, i.e:
        query =  {
            "query": "/radius/add",
            "args": {
                "address": "52.212.123.1",
                "comment": "some_comment"
            }
        }
        """

        if "query" not in query.keys():
            raise QueryException("query statement not found")
        if "args" not in query.keys():
            raise QueryException("missing query arguments")

        self.query = query

    def exec_query(self):
        """
        Execute query and returns the response in a list
        """
        if self.query == {}:
            raise QueryException("no query set")

        try:
            query = self.api(self.query["query"], **self.query["args"])
            resp = []
            for gen in query:
                resp.append(gen)
            return resp
        except Exception:
            raise Exception("unmapped error - could no execute query")

    def api_connect(self):
        """
        function to open a mikrotik connection for api calls
        """

        args = {
            'host': str(self.host_ip),
            'password': self.password,
            'username': self.username,
            'timeout': self.timeout,
            'login_method': self._loginMethods[self.loginMethod],
            'port': self.apiPort
        }

        try:
            self.api = connect(**args)
        except socket.timeout:
            raise socket.timeout(f"mikrotik {self.deviceId} timeout")
        except TrapError as err:
            if "invalid user name or password" in str(err):
                raise MKLoginError(f"invalid username or password")
        except Exception:
            raise Exception(f"unmapped error - could not connect to mikrotik")
