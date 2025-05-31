from models import Users, db, News
from werkzeug.security import generate_password_hash
from manage import minio
from typing import List
from schemas import UserRegisterRequest, PatchUserRequest
from werkzeug.exceptions import NotFound


class UserService:
    @staticmethod
    def get_all_users() -> List[Users]:
        return Users.query.all()

    @staticmethod
    def get_user_by_login(login: str) -> Users:
        return Users.query.filter(Users.login == login).first()

    @staticmethod
    def get_user_by_user_id(user_id: str) -> Users:
        user = Users.query.filter(Users.user_id == user_id).first()

        if user is None:
            raise NotFound("User not found")

        return user

    @staticmethod
    def create_user(body: UserRegisterRequest, is_admin: bool) -> Users:
        password_hash = generate_password_hash(body.password)
        new_user = Users(
            name=body.name,
            surname=body.surname,
            school=body.school,
            building=body.building,
            is_admin=is_admin,
            login=body.login,
            password_hash=password_hash
        )

        if body.avatar_url:
            file = minio.upload_base64(body.avatar_url, body.login)
            file_url = minio.get_public_url(file)
            new_user.avatar_url = file_url

        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def patch_profile(user: Users, body:PatchUserRequest) -> Users:
        attributes = ["name", "surname", "building", "avatar_url", "login"]

        for attr in attributes:
            if hasattr(body, attr) and getattr(body, attr) is not None:
                if attr == "avatar_url":
                    file = minio.upload_base64(body.avatar_url, user.login)
                    file_url = minio.get_public_url(file)
                    user.avatar_url = file_url
                else:
                    setattr(user, attr, getattr(body, attr))

        db.session.commit()
        return user

    @staticmethod
    def is_user_authorized_for_post(user_id: str, post_id: str) -> bool:
        post = News.query.filter_by(post_id=post_id).first()

        if post is None:
            raise NotFound("Post not found")

        if str(post.user_id) == str(user_id):
            return True

        return False

    @staticmethod
    def get_school() -> List[str]:
        schools_query = db.session.query(Users.school) \
            .join(News, Users.user_id == News.user_id) \
            .filter(News.status == "published") \
            .distinct()

        schools = [school[0] for school in schools_query.all()]
        return schools