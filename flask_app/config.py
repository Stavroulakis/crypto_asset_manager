from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))

class Config:
    DB_HOST = environ.get('SECRET_KEY')