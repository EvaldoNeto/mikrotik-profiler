from enum import Enum


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
