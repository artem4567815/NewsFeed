from models import Users, db
from werkzeug.security import generate_password_hash


def get_all_users():
    return Users.query.all()


def find_user_by_login(login):
    return Users.query.filter(Users.login == login).first()

def find_user_by_user_id(user_id):
    return Users.query.filter(Users.user_id == user_id).first()


def create_user(name, surname, school, building, is_admin, login, password):
    password_hash = generate_password_hash(password)
    new_user = Users(name=name, surname=surname, school=school, building=building, is_admin=is_admin, login=login,
                     password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return new_user
