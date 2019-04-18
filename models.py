"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    
    __tablename__= "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(), default="https://d1ejxu6vysztl5.cloudfront.net/lasagna/lasagna2-sm.jpg")

    def __repr__(self):
        return (f"id: {self.id}, first: {self.first_name}, last: {self.last_name}, img: {self.img_url}")

class Post(db.Model):
    __tablename__ = "post"
    user = db.relationship('User', backref='post')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return (f"id: {self.id}, title: {self.title}, content: {self.content}, created at: {self.created_at}, user_id: {self.user_id}")
