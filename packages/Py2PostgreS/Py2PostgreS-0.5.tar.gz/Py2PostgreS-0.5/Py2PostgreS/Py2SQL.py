import psycopg2


def should_be_connected(func):
    def wrapper(*args):
        if args[0].was_connected():
            return func(*args)
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

    @should_be_connected
    def db_disconnect(self):
        self.__was_connected = False
        self.__conn = None

    @should_be_connected
    def db_engine(self):
        cursor = self.__conn.cursor()
        cursor.execute("SELECT version()")
        return cursor.fetchone()[0].split(',')[0]

    @should_be_connected
    def db_name(self):
        cursor = self.__conn.cursor()
        cursor.execute("SELECT current_database()")
        return cursor.fetchone()[0]

    @should_be_connected
    def db_tables(self):
        cursor = self.__conn.cursor()
        cursor.execute("""SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'""")
        tables = cursor.fetchall()
        flatten = lambda t: [item for sublist in t for item in sublist]
        return flatten(tables)

    @should_be_connected
    def db_table_structure(self, table):
        cursor = self.__conn.cursor()
        cursor.execute(f"""SELECT ordinal_position, column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS 
                        WHERE table_name = '{table}'
                        ORDER BY ordinal_position""")
        return cursor.fetchall()

    @should_be_connected
    def db_size(self):
        cursor = self.__conn.cursor()
        cursor.execute(f"""SELECT pg_size_pretty(pg_database_size(db.datname))
                        FROM (SELECT current_database() datname) db""")
        return cursor.fetchone()[0]

    @should_be_connected
    def db_table_size(self, table):
        cursor = self.__conn.cursor()
        cursor.execute(f"""SELECT pg_size_pretty(pg_total_relation_size('{table}'))""")
        return cursor.fetchone()[0]
