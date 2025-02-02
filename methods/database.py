from models import News, Users, db
import os


def get_all_news():
    return News.query.all()     


def get_all_users():
    return Users.query.all()   


def find_user_by_name(name):
    return Users.query.filter(Users.name == name).first()


def find_news_by_id(id):
    return News.query.filter(News.id == id).first()


def find_news_by_user_id(id):
    return News.query.filter(News.user_id == id).all()

def get_latest_file(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if not files:
        return None

    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))

    return os.path.join(directory, latest_file)


def add_to_database2(title, short_content, full_content, image_url, interval, user_id, type):
    new_record = News(title=title, short_content=short_content, content=full_content, image_url=image_url, date_interval=interval, type=type, user_id=user_id)

    db.session.add(new_record)
    db.session.commit()


def to_moderation():
    pass