from models import News, db, UsersHistory
import uuid
from werkzeug.exceptions import BadRequest


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


def patch_post_method(post, body):
    if body.title is not None:
        post.title = body.title
    if body.content is not None:
        post.full_content = body.content
    if body.short_content is not None:
        post.short_content = body.short_content
    if body.end_date is not None:
        post.end_date = body.end_date
    if body.start_date is not None:
        post.start_date = body.start_date
    if body.image_url is not None:
        post.image_url = body.image_url
    if body.tags is not None:
        post.tags = body.tags

    db.session.commit()

    return post


def is_valid_uuid(value):
    uuid_obj = uuid.UUID(value)
    return str(uuid_obj) == value


def like_post_method(post, user_id):
    history = UsersHistory.query.filter_by(user_id=user_id, post_id=post.post_id).first()

    if history is None:
        history = UsersHistory(user_id=user_id, post_id=post.post_id, liked=True)
        db.session.add(history)
    else:
        if history.liked:
            return 204

        history.liked = True

    db.session.commit()


def unlike_post_method(post, user_id):
    history = UsersHistory.query.filter_by(user_id=user_id, post_id=post.post_id).first()

    if history is None or not history.liked:
        raise BadRequest("Like not found")

    history.liked = False
    db.session.commit()


def view_post_method(post, user_id):
    history = UsersHistory.query.filter_by(user_id=user_id, post_id=post.post_id).first()

    if history is None:
        history = UsersHistory(user_id=user_id, post_id=post.post_id, viewed=True)
        db.session.add(history)
    else:
        if history.viewed:
            return 204

        history.viewed = True

    db.session.commit()


def join_post_method(post, user_id):
    history = UsersHistory.query.filter_by(user_id=user_id, post_id=post.post_id).first()

    if history is None:
        history = UsersHistory(user_id=user_id, post_id=post.post_id, joined=True)
        db.session.add(history)
    else:
        if history.joined:
            return 204

        history.joined = True

    db.session.commit()