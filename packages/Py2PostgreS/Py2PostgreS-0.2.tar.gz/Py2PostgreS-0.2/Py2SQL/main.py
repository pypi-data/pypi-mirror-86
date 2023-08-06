# it is just for testing
from Py2SQL import *
from Py2SQL.Py2SQL import Py2SQL

import Py2PostgreS

connection = Py2SQL()
db = {'name': 'postgres', 'user': 'postgres', 'password': 'postgres', 'host': 'localhost'}
connection.db_connect(db)

connection.db_disconnect()