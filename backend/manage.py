from flask import Flask
from models import db
from flask_migrate import Migrate
from config import *
from flask_cors import CORS
import redis
from logger import Logger
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
app.secret_key = APP_SECRET

db_string = "postgresql://{}:{}@{}:{}/{}".format(DB_LOGIN, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SECRET_KEY'] = APP_SECRET
app.config['FLASK_PYDANTIC_VALIDATION_ERROR_RAISE'] = True
app.config['JWT_SECRET_KEY'] = 'very_secret_config'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_REFRESH_COOKIE_NAME'] = "refresh_token_cookie"

db.init_app(app)
migrate = Migrate(app, db)

logger = Logger()

jwt = JWTManager(app)