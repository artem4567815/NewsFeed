from flask import Flask
from models import db
from flask_migrate import Migrate
from config import *
from flask_cors import CORS
import redis

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = APP_SECRET

db_string = "postgresql://{}:{}@{}:{}/{}".format(DB_LOGIN, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SECRET_KEY'] = APP_SECRET

db.init_app(app)
migrate = Migrate(app, db)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
