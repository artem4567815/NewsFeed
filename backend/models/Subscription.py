from . import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY

class Subscription(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    user_id = db.Column(UUID, db.ForeignKey('users.user_id'), nullable=False)
    tags = db.Column(ARRAY(db.String), nullable=True)
    authors = db.Column(ARRAY(db.String), nullable=True)

    all = db.Column(db.Boolean, nullable=True, default=False)

    def as_dict(self):
        result = {
            'user_id': self.user_id,
        }

        if self.tags:
            result['tags'] = self.tags
        if self.authors:
            result['authors'] = self.authors

        return result