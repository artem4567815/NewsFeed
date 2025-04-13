from models  import News, db, UsersHistory, Users
from datetime import datetime
from sqlalchemy import func


def get_most_three_active_user():
    result = db.session.query(
        News.user_id,
        Users.login,
        func.count(News.post_id).label('total_posts')
    ).join(
        Users,
        News.user_id == Users.user_id
    ).group_by(
        News.user_id,
        Users.login
    ).filter(
        Users.is_admin == False
    ).limit(3).all()

    out = [
        {
            "id": user[0],
            "login": user[1],
            "post_count": user[2],
        }
        for user in result
    ]
    print(out)
    out = sorted(out, key=lambda x: x["post_count"], reverse=True)
    print(out)

    return out


def get_expired_posts_avg_conversion(user_id):
    current_timestamp = int(datetime.now().timestamp())

    expired_posts = db.session.query(News).filter(
        News.end_date < current_timestamp,
        News.user_id == user_id
    ).all()

    total_conversion = 0

    for post in expired_posts:
        likes_count = db.session.query(func.count(UsersHistory.id)).filter(
            UsersHistory.post_id == post.id,
            UsersHistory.liked == True
        ).scalar()

        joins_count = db.session.query(func.count(UsersHistory.id)).filter(
            UsersHistory.post_id == post.id,
            UsersHistory.joined == True
        ).scalar()

        conversion = joins_count / likes_count if likes_count > 0 else 0
        total_conversion += conversion

    avg_conversion = total_conversion / len(expired_posts) if expired_posts else 0

    return avg_conversion


def get_statistics_by_posts_id(post_id):
    likes_count = db.session.query(func.count(UsersHistory.id)).filter(
        UsersHistory.post_id == post_id,
        UsersHistory.liked == True
    ).scalar()

    joins_count = db.session.query(func.count(UsersHistory.id)).filter(
        UsersHistory.post_id == post_id,
        UsersHistory.joined == True
    ).scalar()

    # views_count = db.session.query(func.count(UsersHistory.id)).filter(
    #     UsersHistory.post_id == post_id,
    #     UsersHistory.viewed == True
    # ).scalar()
    views_count = db.session.query(News).filter_by(post_id=post_id).first().views

    conversion = joins_count / likes_count if likes_count > 0 else 0

    return {
        "likes": likes_count,
        "views": views_count,
        "conversion": conversion,
        "joined": joins_count
    }
