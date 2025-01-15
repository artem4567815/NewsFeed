from . import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    corpus = db.Column(db.String(100), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False)

    credentials = db.relationship('Credentials', backref='user', uselist=False)
    news = db.relationship('News', backref='users')

