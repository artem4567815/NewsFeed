from . import db, UsersHistory
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.dialects.postgresql import ARRAY

class News(db.Model):
    post_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    title = db.Column(db.String(100), nullable=False)
    short_content = db.Column(db.Text, nullable=False)
    full_content = db.Column(db.Text, nullable=False)

    start_date = db.Column(db.BigInteger, nullable=True)
    end_date = db.Column(db.BigInteger, nullable=True)

    image_url = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)
    type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False, default='draft')
    tags = db.Column(ARRAY(db.String))

    user_id = db.Column(db.UUID, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)

    user_history = db.relationship('UsersHistory', backref='post', uselist=True)

    def as_dict(self):
        result =  {
            "post_id": self.post_id,
            "title": self.title,
            "short_content": self.short_content,
            "full_content": self.full_content,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "image_url": self.image_url,
            "type": self.type,
            "status": self.status,
            "author": {
                "id": self.user_id,
                "login": self.user.login,
            },
            "created_at": self.created_at,
            "likes_count": len([x for x in self.user_history if x.liked and x.post_id == self.post_id]),
            "views": len([x for x in self.user_history if x.viewed and x.post_id == self.post_id])
        }

        if self.user.avatar_url is not None:
            result['author']['avatar_url'] = self.user.avatar_url

        if self.tags is not None:
            result['tags'] = self.tags

        return result
