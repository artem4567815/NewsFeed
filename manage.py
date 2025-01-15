from flask import Flask, redirect, session
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from models import db, Credentials
from werkzeug.security import check_password_hash
from flask_migrate import Migrate
from config import *

app = Flask(__name__)
app.secret_key = APP_SECRET

db_string = "postgresql://{}:{}@{}:{}/{}".format(DB_LOGIN, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SECRET_KEY'] = APP_SECRET

login_manager = LoginManager(app)
login_manager.login_view = '/routes/login'

class User(UserMixin):
    def __init__(self, user):
        self.id = user.user_id
        self.username = user.login
        self.password_hash = user.password_hash
        self.is_admin = user.user.is_admin
        print(f"{self.id} {self.username} {self.password_hash}")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    

@login_manager.user_loader
def load_user(user_id):
    credentials = Credentials.query.filter_by(user_id=user_id).first()
    if credentials:
        return User(credentials)
    return None


db.init_app(app)
migrate = Migrate(app, db)
