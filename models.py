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
    post_tags = db.relationship('PostTag', backref='post')
    tags = db.relationship('Tag', secondary='post_tags', backref='post')

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


class Tag(db.Model):
    """Tags for posts"""
    __tablename__ = "tag"
    post_tags = db.relationship('PostTag', backref='tag')
    posts = db.relationship('Post', secondary='post_tags', backref='tag')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return (f"id: {self.id}, name: {self.name}")

class PostTag(db.Model):
    __tablename__ = "post_tags"
    

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)

    def __repr__(self):
        return f"post_id: {self.post_id}"
################################################################################################################################################################
# refactor table names

print("!!!~~~~~~~ LOOK HERE: we're running the updated")