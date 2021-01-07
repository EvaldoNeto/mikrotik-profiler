"""
For now just some examples on how to do it
"""

def api_calls(api_name: str) -> dict:
    """
    Here we register all possible apis
    """
    apis = {
        "interface_print": {
            "query": "/interface/print",
            "args": {}
        },
        "interface_get": {
            "query": "/interface/get",
            "args": {
                "number": "ether1"
            }
        }
    }

    return apis[api_name]