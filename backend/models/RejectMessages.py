from . import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class RejectMessages(db.Model):
    message_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    post_id = db.Column(db.UUID, db.ForeignKey('news.post_id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.UUID, db.ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)

    reason = db.Column(db.String, nullable=False)

    def as_dict(self):
        return self.reason
