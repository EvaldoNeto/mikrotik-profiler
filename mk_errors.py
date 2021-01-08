

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
