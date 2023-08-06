import os
from inspect import isclass

import psycopg2


def should_be_connected(func):
    def wrapper(*args):
        if args[0].was_connected():
            return func(*args)
        else:
            raise RuntimeError("wasn't connected")

    return wrapper


class Py2SQL:
    def __init__(self):
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

    @should_be_connected
    def find_class(self, py_class):
        if not isclass(py_class):
            raise RuntimeError('is not class')
        structure = self.db_table_structure(py_class.__name__.lower())
        columns = map(lambda x: x[1], structure)

        result = []
        for key, value in py_class().__dict__.items():
            if key not in columns:
                return
            result.append((key, list(filter(lambda x: x[1] == key, structure))[0][2]))

        if len(result) == len(structure):
            return result

    @should_be_connected
    def create_class(self, table, module, _globals=None):
        structure = self.db_table_structure(table)
        fields = list(map(lambda x: x[1], structure))
        init_list = ''
        for field in fields:
            init_list += ', ' + field
        if not os.path.exists(module):
            os.makedirs(module)
        try:
            file = open(f'./{module}/' + table + '.py', 'x')
            file.write(f'\nclass {table.capitalize()}:\n\n')
            file.write(f'    def __init__(self{init_list}):\n')
            for field in fields:
                file.write(f'        self.{field} = {field}\n')
            file.close()
            exec(f'from {module.replace("/", ".")}.{table} import {table.capitalize()}', _globals)
        except FileExistsError as e:
            raise RuntimeError(e)
