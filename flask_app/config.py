from os import environ, path
from dotenv import load_dotenv
import os
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    DB_HOST = environ.get('DB_HOST')
    DB_PORT = environ.get('DB_PORT')
    DB_USER = environ.get('DB_USER')
    DB_PASSWORD = environ.get('DB_PASSWORD')
    DB_DATABASE = environ.get('DB_DATABASE')
    SECRET_KEY = os.urandom(32)
    DEBUG=True
    BINANCE_SECRET_KEY = environ.get('BINANCE_SECRET_KEY')
    BINANCE_API_KEY = environ.get('BINANCE_API_KEY')