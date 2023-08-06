import psycopg2


def should_be_connected(func):
    def wrapper(*args):
        if args[0].was_connected():
            return func(args)
        else:
            raise RuntimeError("wasn't connected")

    return wrapper


class Py2SQL:
    __was_connected = False
    __conn = None

    def was_connected(self):
        return self.__was_connected

    def db_connect(self, db):
        self.__conn = psycopg2.connect(dbname=db['name'], user=db['user'],
                                       password=db['password'], host=db['host'])
        self.__was_connected = True

    # @should_be_connected
    def db_disconnect(self):
        self.__was_connected = False
        self.__conn = None
