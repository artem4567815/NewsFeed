from flask import Flask, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from models import db
from flask_migrate import Migrate
from config import *

app = Flask(__name__)

db_string = "postgresql://{}:{}@{}:{}/{}".format(DB_LOGIN, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SECRET_KEY'] = APP_SECRET

login_manager = LoginManager(app)
login_manager.login_view = '/admin/login'

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.username = ADMIN_USERNAME
        self.password = ADMIN_PASSWORD_HASH

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


db.init_app(app)
migrate = Migrate(app, db)
