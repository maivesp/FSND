
import os
SECRET_KEY = os.urandom(32)
#  Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable the debug mode
DEBUG = True

# Connect to the database

DB_HOST =os.getenv('DB_HOST','127.0.0.1:5432')
DB_USER = os.getenv('DB_USER','postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD','postgres')
DB_NAME = os.getenv('DB_NAME','moviedb')
DB_PATH = 'postgresql+psycopg2:/{}:{}@{}/{}'.format(DB_USER,DB_PASSWORD,DB_HOST,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_PATH
import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/moviedb'
SQLALCHEMY_TRACK_MODIFICATIONS = False


