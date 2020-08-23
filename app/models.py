from app import db
from datetime import datetime
from flask_login import UserMixin


class Article(db.Model):
    __tablename__ = 'Article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __repr__(self):
        return f'<ARTICLE {self.id}|{self.title}>'


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    image = db.Column(db.BLOB)
    pr = db.relationship('Article', backref='User')
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def has_admin(self):
        return True if self.admin else False

    def get_id(self):
        return self.id

    def __repr__(self):
        return f'<USER {self.id}|{self.username}>'

