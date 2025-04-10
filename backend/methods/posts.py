from models import News, db
from sqlalchemy import select


def get_all_news():
    return News.query.all()


def get_news_by_query(query):
    posts = News.query

    if query.type is not None:
        posts = posts.filter_by(type=query.type)

    if query.start_date is not None:
        posts = posts.filter(News.start_date >= int(query.start_date))
    if query.end_date is not None:
        posts = posts.filter(News.end_date <= int(query.end_date))

    if query.tags is not None:
        posts = posts.where(News.tags.overlap(query.tags))

    posts = posts.offset(query.offset).limit(query.limit).all()
    return posts


def find_news_by_id(post_id):
    return News.query.filter(News.post_id == post_id).first()


def find_news_by_user_id(user_id):
    return News.query.filter(News.user_id == user_id).all()


def create_news(title, short_content, full_content, image_url, start_date,
                end_date, user_id, type_field, tags, status="published"):
    new_record = News(title=title, short_content=short_content, full_content=full_content,
                      start_date=start_date,
                      end_date=end_date,
                      image_url=image_url,
                      type=type_field, user_id=user_id,
                      status=status)

    if tags is not None:
        new_record.tags = tags

    db.session.add(new_record)
    db.session.commit()

    return new_record
