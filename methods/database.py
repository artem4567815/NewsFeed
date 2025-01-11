from models import NewsFiles, News, db
import os

def get_all_news_files():
    return NewsFiles.query.all()

def get_all_news():
    return News.query.all()       

def get_latest_file(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if not files:
        return None

    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))

    return os.path.join(directory, latest_file)


def add_to_database(news_file):
    new_record = NewsFiles(name='canvas', image_url=news_file)

    db.session.add(new_record)
    db.session.commit()


def add_to_database2(title, short_content, full_content, image_url):
    new_record = News(title=title, short_content=short_content, content=full_content, image_url=image_url)

    db.session.add(new_record)
    db.session.commit()

def search_filename(filename_path):
    if not NewsFiles.query.filter_by(image_url=filename_path).first():
        return False
    return True
