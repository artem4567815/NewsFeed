from models import Users, db
from werkzeug.security import generate_password_hash
from manage import minio


def get_all_users():
    return Users.query.all()


def find_user_by_login(login):
    return Users.query.filter(Users.login == login).first()


def find_user_by_user_id(user_id):
    return Users.query.filter(Users.user_id == user_id).first()


def create_user(name, surname, school, building, is_admin, login, password, avatar_url):
    password_hash = generate_password_hash(password)
    new_user = Users(name=name, surname=surname, school=school, building=building, is_admin=is_admin, login=login,
                     password_hash=password_hash)

    if avatar_url is not None:
        file = minio.upload_base64(avatar_url, login)
        file_url = minio.get_public_url(file)
        new_user.avatar_url = file_url

    db.session.add(new_user)
    db.session.commit()

    return new_user


def patch_profile_method(user, body):
    if body.name is not None:
        user.name = body.name
    if body.surname is not None:
        user.surname = body.surname
    if body.building is not None:
        user.building = body.building
    if body.avatar_url is not None:
        file = minio.upload_base64(body.avatar_url, user.login)
        file_url = minio.get_public_url(file)
        user.avatar_url = file_url
    if body.login is not None:
        user.login = body.login

    db.session.commit()

    return user
