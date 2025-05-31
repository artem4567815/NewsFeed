from models import Subscription, db, Users
from methods import PostService
from werkzeug.exceptions import BadRequest

class SubscribeService:
    @staticmethod
    def remove_existing_subscription(user_id):
        existing = Subscription.query.filter_by(user_id=user_id).first()
        if existing:
            db.session.delete(existing)

    @staticmethod
    def validate_tags(tags):
        if not tags:
            return []

        available_tags = PostService.get_tags()
        invalid = [tag for tag in tags if tag not in available_tags]
        if invalid:
            raise BadRequest(f"Invalid tags: {', '.join(invalid)}")

        return tags

    @staticmethod
    def validate_authors(authors):
        if not authors:
            return []

        found = Users.query.filter(Users.login.in_(authors)).all()
        found_logins = [a.login for a in found]
        missing = [a for a in authors if a not in found_logins]

        if missing:
            raise BadRequest(f"Authors not found: {', '.join(missing)}")

        return found_logins

    @staticmethod
    def create_subscription(user_id, tags, authors):
        new_sub = Subscription(user_id=user_id, tags=tags, authors=authors)
        db.session.add(new_sub)
        db.session.commit()

    @staticmethod
    def get_subscription(user_id: str) -> Subscription:
        subscribe = Subscription.query.filter_by(user_id=user_id).first()

        if not subscribe:
            raise BadRequest(f"Subscription not found: {user_id}")

        return subscribe