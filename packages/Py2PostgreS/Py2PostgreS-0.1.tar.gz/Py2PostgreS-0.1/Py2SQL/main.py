# it is just for testing
from Py2SQL import Py2SQL

connection = Py2SQL()
db = {'name': 'postgres', 'user': 'postgres', 'password': 'postgres', 'host': 'localhost'}
connection.db_connect(db)

connection.db_disconnect()