from models import News, db
import os

def get_all_news():
    return News.query.all()       

def get_latest_file(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if not files:
        return None

    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))

    return os.path.join(directory, latest_file)


def add_to_database2(title, short_content, full_content, image_url, interval):
    new_record = News(title=title, short_content=short_content, content=full_content, image_url=image_url, date_interval=interval)

    db.session.add(new_record)
    db.session.commit()