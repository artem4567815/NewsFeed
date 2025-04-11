from models  import News, db
from sqlalchemy import func


def get_most_active_user():
    result = db.session.query(
        News.user_id,
        News.user.login,
        func.count(News.post_id).label('total_posts')
    ).group_by(News.user_id).order_by(
        func.count(News.post_id).desc()
    ).limit(1).first()

    return {
        "id": result.user_id,
        "login": result.user.login,
        "post_count": result.total_posts,
    }
