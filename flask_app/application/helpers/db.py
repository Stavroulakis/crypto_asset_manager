import mysql.connector
from flask import current_app

# connect to the sql db
def db_connect():
    connection = mysql.connector.connect(host = current_app.config['db_host'],
                                         port = current_app.config['db_port'],
                                         user = current_app.config['db_user'],
                                         password = current_app.config['db_pass'],
                                         database = current_app.config['db_name'])
    cursor = connection.cursor(buffered=True , dictionary=True)
    return cursor