from models import News, db


def get_all_news():
    return News.query.all()


def get_news_for_category(category):
    return News.query.filter_by(type=category).all()


def find_news_by_id(post_id):
    return News.query.filter(News.news_id == post_id).first()


def find_news_by_user_id(user_id):
    return News.query.filter(News.user_id == user_id).all()


def create_news(title, short_content, full_content, image_url, interval, user_id, type_field):
    new_record = News(title=title, short_content=short_content, content=full_content, image_url=image_url,
                      date_interval=interval, type=type_field, user_id=user_id)

    db.session.add(new_record)
    db.session.commit()

    return new_record
