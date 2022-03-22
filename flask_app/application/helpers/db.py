import mysql.connector
from flask import current_app

# connect to the sql db
def db_connect():
    connection = mysql.connector.connect(host = current_app.config['DB_HOST'],
                                         port = current_app.config['DB_PORT'],
                                         user = current_app.config['DB_USER'],
                                         password = current_app.config['DB_PASSWORD'],
                                         database = current_app.config['DB_DATABASE'],auth_plugin='mysql_native_password')
    cursor = connection.cursor(buffered=True , dictionary=True)
    return connection, cursor