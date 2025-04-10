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
CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = APP_SECRET

db_string = "postgresql://{}:{}@{}:{}/{}".format(DB_LOGIN, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SECRET_KEY'] = APP_SECRET
app.config['FLASK_PYDANTIC_VALIDATION_ERROR_RAISE'] = True
app.config['JWT_SECRET_KEY'] = 'very_secret_config'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)


db.init_app(app)
migrate = Migrate(app, db)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

logger = Logger()

jwt = JWTManager(app)