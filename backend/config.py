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

DEBUG = int(os.getenv("FLASK_DEBUG", "0"))
SERVER_ADD = os.getenv('SERVER_ADD', "/api")
JWT_SECRET = os.getenv('JWT_SECRET') if not DEBUG else "test_jwt_in_debug"
UPLOAD_FOLDER = "images"


access_key = os.getenv("access_key")
secret_key = os.getenv("secret_key")
endpoint = os.getenv("endpoint")
test_bucket = os.getenv("test_bucket")
bucket = os.getenv("bucket") if not DEBUG else test_bucket
