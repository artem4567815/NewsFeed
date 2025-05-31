from typing import List, Tuple
from pydantic.v1 import UUID4
from models import News, db, UsersHistory, Users, RejectMessages
import uuid
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy import or_, func
from schemas import QueryRequest, CreateNewsRequest, PatchPostRequest
from datetime import datetime
from manage import minio
from urllib.parse import urlparse

class PostService:
    @staticmethod
    def get_all_news() -> List[News]:
        return News.query.all()

    @staticmethod
    def get_all_news_by_status(status: str) -> List[dict[News]]:
        posts = News.query.filter_by(status=status).all()
        return [post.as_dict() for post in posts]

    @staticmethod
    def get_news_by_query(params: QueryRequest) -> Tuple[List[dict[News]], int]:
        query = News.query.filter_by(status="published")

        if params.type:
            types = params.type.split(',')
            query = query.where(News.type.in_(types))

        if params.start_date:
            query = query.filter(News.start_date >= int(params.start_date))
        if params.end_date:
            query = query.filter(News.end_date <= int(params.end_date))

        if params.tags:
            tags = params.tags.split(',')
            query = query.where(News.tags.overlap(tags))

        if params.school:
            query = query.join(Users).filter(Users.school == params.school)

        if params.search:
            query = query.filter(
                or_(News.title.contains(params.search), News.short_content.contains(params.search))
            )

        query = query.order_by(News.published_at.desc())
        posts_count = query.count()

        if params.offset:
            query = query.offset(params.offset)

        if params.limit:
            query = query.limit(params.limit)

        return [news.as_dict() for news in query.all()], posts_count

    @staticmethod
    def get_news_by_post_id(post_id: str) -> News:
        post = News.query.filter(News.post_id == post_id).first()

        if not post:
            raise NotFound("Post not found")

        return post

    @staticmethod
    def get_news_by_user_id(user_id: str) -> List[dict[News]]:
        posts = News.query.filter(News.user_id == user_id).all()

        if not posts:
            raise NotFound("Posts by this user not found")

        posts = [post.as_dict() for post in posts]
        posts = sorted(posts, key=lambda news: news["created_at"], reverse=False)

        return posts

    @staticmethod
    def create_news(body: CreateNewsRequest, image_url: str, user_id: UUID4, status: str) -> News:
        new_record = News(
            title=body.title,
            short_content=body.short_content,
            full_content=body.content,
            start_date=body.start_date,
            end_date=body.end_date,
            image_url=image_url,
            type=body.type,
            user_id=user_id,
            status=status
        )

        if body.tags:
            new_record.tags = body.tags

        if status == "published":
            new_record.published_at = func.now()

        db.session.add(new_record)
        db.session.commit()

        return new_record

    @staticmethod
    def patch_post(post: News, body: PatchPostRequest) -> News:
        attributes = ["title", "content", "short_content", "end_date", "start_date", "image_url", "tags"]

        for attr in attributes:
            if hasattr(body, attr) and getattr(body, attr) is not None:
                setattr(post, attr if attr != "content" else "full_content", getattr(body, attr))

        db.session.commit()
        return post

    @staticmethod
    def is_valid_uuid(value: str) -> None:
        uuid_obj = uuid.UUID(value)
        if str(uuid_obj) != value:
            raise ValueError("Invalid UUID")

    @staticmethod
    def post_action(post: News, user_id: str, action: str) -> int:
        valid_actions = {"liked", "joined"}
        if action not in valid_actions:
            raise ValueError(f"Invalid action: {action}. Must be one of {valid_actions}.")

        history = UsersHistory.query.filter_by(user_id=user_id, post_id=post.post_id).first()

        if history is None:
            history = UsersHistory(user_id=user_id, post_id=post.post_id, **{action: True})
            db.session.add(history)
        else:
            if getattr(history, action):
                return 204

            setattr(history, action, True)

        db.session.commit()

    @staticmethod
    def like_post(post: News, user_id: str) -> int:
        return PostService.post_action(post, user_id, "liked")

    @staticmethod
    def unlike_post(post: News, user_id: str):
        history = UsersHistory.query.filter_by(user_id=user_id, post_id=post.post_id).first()

        if history is None or not history.liked:
            raise BadRequest("Like not found")

        history.liked = False
        db.session.commit()

    @staticmethod
    def join_post(post: News, user_id: str) -> int:
        return PostService.post_action(post, user_id, "joined")


    @staticmethod
    def reject(reasons: List[str], post_id: str, user_id: str):
        post = PostService.get_news_by_post_id(post_id)

        if not isinstance(reasons, list) or not all(isinstance(r, str) for r in reasons) or not reasons:
            raise BadRequest("Invalid reason format. Must be a list of strings.")

        post.status = "rejected"
        RejectMessages.query.filter_by(post_id=post_id).delete()
        reject_entries = [RejectMessages(reason=r, post_id=post_id, user_id=user_id) for r in reasons]
        db.session.bulk_save_objects(reject_entries)
        db.session.commit()

    @staticmethod
    def apply(post_id: str):
        post = PostService.get_news_by_post_id(post_id)

        post.status = "published"
        post.published_at = func.now()
        db.session.commit()

    @staticmethod
    def join(post: News, user_id: str):
        current_timestamp = int(datetime.now().timestamp())
        if post.type == "news":
            if current_timestamp > post.end_date:
                raise BadRequest("Ты уже не можешь присоединиться, событие прошло")
            PostService.join_post(post, user_id)
        else:
            raise BadRequest("Присоединиться можно только к событию")

    @staticmethod
    def get_tags() -> List[str]:
        tags_query = db.session.query(func.unnest(News.tags)) \
            .filter(News.status == "published") \
            .distinct()
        tags = [tag[0] for tag in tags_query.all()]
        return tags

    @staticmethod
    def resolve_file_url(post_img: str, username: str) -> str:
        if PostService.is_url(post_img):
            return post_img

        file = minio.upload_base64(post_img, username)
        return minio.get_public_url(file)

    @staticmethod
    def is_url(value: str) -> bool:
        parsed = urlparse(value)
        return parsed.scheme in ('http', 'https') and bool(parsed.netloc)
