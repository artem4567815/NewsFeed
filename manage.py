from flask import Flask
from flask_login import LoginManager, UserMixin
from models import db, Users
from werkzeug.security import check_password_hash
from flask_migrate import Migrate
from config import *

app = Flask(__name__)
app.secret_key = APP_SECRET

db_string = "postgresql://{}:{}@{}:{}/{}".format(DB_LOGIN, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SECRET_KEY'] = APP_SECRET

login_manager = LoginManager(app)
login_manager.login_view = '/auth/login'

class User(UserMixin):
    def __init__(self, user):
        self.id = user.id
        self.username = user.login
        self.password_hash = user.password_hash
        self.is_admin = user.is_admin
        print(f"{self.id} {self.username} {self.password_hash}")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    

@login_manager.user_loader
def load_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if user:
        return User(user)
    return None


db.init_app(app)
migrate = Migrate(app, db)
