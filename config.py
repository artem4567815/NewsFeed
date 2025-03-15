import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_PORT = os.environ.get('DB_PORT')
DB_LOGIN = os.environ.get('DB_LOGIN')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
APP_SECRET = os.environ.get('APP_SECRET')
SERVER_PORT = os.getenv('SERVER_PORT', 8080)

PORT = 1234

DEBUG = True

UPLOADFLOADER = 'images'
