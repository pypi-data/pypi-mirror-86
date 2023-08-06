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
    def find_objects_by(self, table, attributes):
        params_value = {'field__gt': '>', 'field__lt': '<',
                        'field__gte': '>=', 'field__lte': '<=',
                        'field__in': 'IN', 'field__not_in': 'NOT IN'}
        if not isinstance(attributes, list):
            raise RuntimeError('Attributes type error')
        for attr in attributes:
            if not isinstance(attr, tuple) or len(attr) not in (2, 3):
                raise RuntimeError('Attribute type error')
        cursor = self.__conn.cursor()
        query = f"SELECT * from {table}"
        if len(attributes) > 0:
            query += " WHERE "

            query_params = []
            for attr in attributes:
                condition = '='
                if len(attr) == 3 and attr[2] in params_value:
                    condition = params_value[attr[2]]
                if 'IN' in condition:
                    query_params.append(f"{attr[0]} {condition} {tuple(attr[1])}")
                else:
                    query_params.append(f"{attr[0]} {condition} '{attr[1]}'")
            query += ' AND '.join(query_params)
        cursor.execute(query)
        return cursor.fetchall()

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

    @should_be_connected
    def find_object(self, table, py_object):
        cursor = self.__conn.cursor()
        query = f"SELECT exists(SELECT 1 FROM {table}"
        params = py_object.__dict__
        if len(params) > 0:
            query += ' WHERE '
            query_params = []
            for key in params:
                query_params.append(f"{key} {'IS' if params[key] is None else '='} %s")
            query += ' AND '.join(query_params)
        query += ')'
        cursor.execute(query, list(params.values()))
        if cursor.fetchone()[0]:
            cursor.execute(f"""SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS
                                    WHERE table_name = '{table}'
                                    ORDER BY ordinal_position""")
            result = cursor.fetchall()
            i = 0
            values = list(params.values())
            while i < len(result):
                result[i] += (values[i],)
                i += 1
            return result

    @should_be_connected
    def find_hierarches(self):
        cursor = self.__conn.cursor()
        cursor.execute("""WITH RECURSIVE ref (tbl, reftbl, depth,path, cycle) AS (
            SELECT pg_class.oid, NULL::oid, 0, ARRAY[pg_class.OID], false
            FROM pg_class
                     JOIN pg_namespace ON
                pg_namespace.oid = pg_class.relnamespace
            WHERE relkind = 'r'
              AND nspname = 'public'
              AND NOT EXISTS(
                    SELECT 1
                    FROM pg_constraint
                    WHERE conrelid = pg_class.oid
                      AND contype = 'f'
                )
            UNION ALL
            SELECT conrelid, ref.tbl, ref.depth + 1, path || conrelid, conrelid = ANY (path)
            FROM ref
                     JOIN pg_constraint ON
                    confrelid = ref.tbl AND
                    contype = 'f'
            AND NOT cycle
        )
        SELECT tbl::regclass::text                              as tablename,
               string_agg(DISTINCT reftbl::regclass::text, ',') as reftables,
               max(depth)
        FROM ref
        GROUP BY tablename
        ORDER BY max(depth) DESC
        """)
        tables = cursor.fetchall()
        return Py2SQL._get_hierarchies(Py2SQL._to_dict(tables), Py2SQL._get_root(tables))

    @staticmethod
    def _to_dict(tables):
        dictionary = dict()
        for table in tables:
            dictionary[table[0]] = None if table[1] is None else list(table[1].split(','))
        return dictionary

    @staticmethod
    def _get_root(tables):
        max_depth = tables[0][2]
        root = list()
        for table in tables:
            if table[2] == max_depth:
                root.append(table[0])
        return root

    @staticmethod
    def _get_hierarchies(dictionary, root):
        visited = dict()
        for value in list(dictionary.keys()):
            visited[value] = False
        result = list()
        for value in root:
            if not visited[value]:
                result.extend(Py2SQL._find_hierarchy(value, dictionary, visited))
        return result

    @staticmethod
    def _find_hierarchy(value, dictionary, visited):
        result = list()
        visited[value] = True
        if dictionary[value] is not None:
            for i in dictionary[value]:
                if not visited[i]:
                    visited[i] = True
                    results = Py2SQL._find_hierarchy(i, dictionary, visited)
                    if len(results) == 0:
                        result.append([(value, i)])
                    else:
                        for part_result in results:
                            current_result = [(value, i)]
                            current_result.extend(part_result)
                            result.append(current_result)

        return result
