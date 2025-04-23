from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Users(db.Model):
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False)

    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    avatar_url = db.Column(db.String(300), nullable=True)

    news = db.relationship('News', backref='user', uselist=True)
    users_history = db.relationship('UsersHistory', backref='user', uselist=True)
    subscription = db.relationship('Subscription', backref='user', uselist=False)
    message = db.relationship('RejectMessages', backref='user', uselist=True)

    def as_dict(self):
        result = {
            "user_id": self.user_id,
            "name": self.name,
            "surname": self.surname,
            "school": self.school,
            "building": self.building,
            "login": self.login,
        }

        if self.avatar_url is not None:
            result['avatar_url'] = self.avatar_url

        return result
