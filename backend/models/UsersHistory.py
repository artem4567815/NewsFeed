from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UsersHistory(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    user_id = db.Column(UUID, db.ForeignKey('users.user_id', ondelete="CASCADE"))
    post_id = db.Column(UUID, db.ForeignKey('news.post_id', ondelete="CASCADE"))

    liked = db.Column(db.Boolean, default=False)
    joined = db.Column(db.Boolean, default=False)
