from flask import Flask, request
from models import db
from flask_migrate import Migrate
from config import *
from flask_cors import CORS
from logger import Logger
from flask_jwt_extended import JWTManager
from datetime import timedelta
from helpers import MinioClient
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173", "https://edufeed.ru"])
app.secret_key = APP_SECRET

db_string = "postgresql://{}:{}@{}:{}/{}".format(DB_LOGIN, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SECRET_KEY'] = APP_SECRET
app.config['FLASK_PYDANTIC_VALIDATION_ERROR_RAISE'] = True
app.config['JWT_SECRET_KEY'] = JWT_SECRET
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_COOKIE_SECURE'] = bool(not DEBUG)
app.config['JWT_COOKIE_CSRF_PROTECT'] = bool(not DEBUG)
app.config['JWT_REFRESH_COOKIE_NAME'] = "refresh_token_cookie"


app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30
app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800

db.init_app(app)
migrate = Migrate(app, db)

logger = Logger()

jwt = JWTManager(app)

minio = MinioClient(
    access_key=access_key,
    secret_key=secret_key,
    endpoint=endpoint,
    bucket=bucket,
)

@app.after_request
def log_request(response):
    timestamp = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    log_line = (
        f'{request.remote_addr} - - [{timestamp}] '
        f'"{request.method} {request.path} HTTP/1.1" {response.status_code} -'
    )
    logger.log("info", log_line)
    return response
