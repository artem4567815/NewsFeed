from . import db

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    short_content = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_interval = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
