from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class News(db.Model):
    news_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    title = db.Column(db.String(100), nullable=False)
    short_content = db.Column(db.Text, nullable=False)
    full_content = db.Column(db.Text, nullable=False)

    start_date = db.Column(db.Integer, nullable=False)
    end_date = db.Column(db.Integer, nullable=False)

    image_url = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)
    type = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.UUID, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)

    def as_dict(self):
        return {
            "news_id": self.news_id,
            "title": self.title,
            "short_content": self.short_content,
            "full_content": self.full_content,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "image_url": self.image_url,
            "type": self.type,
            "author": {
                "id": self.user_id,
                "name": self.user.name,
                "surname": self.user.surname,
                "avatar_url": "string"
            },
            "created_at": self.created_at
        }
