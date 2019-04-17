"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__= "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(), default="https://d1ejxu6vysztl5.cloudfront.net/lasagna/lasagna2-sm.jpg")

    def __repr__(self):
        return (f"id: {self.id}, first: {self.first_name}, last: {self.last_name}, img: {self.img_url}")


