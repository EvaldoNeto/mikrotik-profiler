"""
Here we just call the mikrotik profile api and send the data retrieved to
the database
"""

from librouteros import connect
from librouteros.login import plain


def mk_connect(
    username: str="admin",
    password: str="",
    host: str="localhost",
    timeout: int=10,
    port: int=28728
):
    """
    simple function to connect to a mikrotik and return a timeout error
    """
    method = plain
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
    except Exception as err:
        raise Exception(err)

