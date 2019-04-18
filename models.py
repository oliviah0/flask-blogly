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

    @property
    def full_name(self):
        """Return full name of user. """
        
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    __tablename__ = "post"
    user = db.relationship('User', backref='post')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    @property
    def formatted_date(self):
        """Return a formatted date. """

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")
    def __repr__(self):
        return (f"id: {self.id}, title: {self.title}, content: {self.content}, created at: {self.formatted_date}, user_id: {self.user_id}")
