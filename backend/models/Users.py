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

    news = db.relationship('News', backref='user', uselist=True)

    def as_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "surname": self.surname,
            "school": self.school,
            "building": self.building,
            "login": self.login,
        }
