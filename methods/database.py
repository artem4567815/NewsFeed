from models import News, Users, db
import os
from werkzeug.security import generate_password_hash


def get_all_news():
    return News.query.all()     


def get_all_users():
    return Users.query.all()   


def find_user_by_login(login):
    return Users.query.filter(Users.login == login).first()


def find_news_by_id(post_id):
    return News.query.filter(News.id == post_id).first()


def find_news_by_user_id(user_id):
    return News.query.filter(News.user_id == user_id).all()

def get_latest_file(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if not files:
        return None

    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))

    return os.path.join(directory, latest_file)


def add_to_database(title, short_content, full_content, image_url, interval, user_id, type_field):
    new_record = News(title=title, short_content=short_content, content=full_content, image_url=image_url,
                      date_interval=interval, type=type_field, user_id=user_id)

    db.session.add(new_record)
    db.session.commit()


def create_user(name, surname, school, corpus, is_admin, login, password):
    password_hash = generate_password_hash(password)
    new_user = Users(name=name, surname=surname, school=school, corpus=corpus, is_admin=is_admin, login=login,
                     password_hash=password_hash)
    print(is_admin)
    db.session.add(new_user)
    db.session.commit()


def to_moderation():
    pass
