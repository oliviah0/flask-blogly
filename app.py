"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET_GARFIELD"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/users')
def index():
    """Routing for Users list """

    users = User.query.all()
    return render_template("index.html", users=users)


@app.route('/users/create', methods=["GET", "POST"])
def create_user():
    """Routing for creating a user """

    if request.method == "POST":
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        img_url = request.form['img-url']
        img_url = img_url if img_url else None

        user = User(first_name=first_name,
                    last_name=last_name, img_url=img_url)
        db.session.add(user)
        db.session.commit()
        print(user)

        return redirect('/users')

    return render_template('create-user.html')


@app.route('/users/user/<int:id>')
def user(id):
    """Routing for viewing a user """

    user = User.query.get(id)
    return render_template('user.html', user=user)


@app.route('/users/user/<int:id>/delete')
def delete(id):
    """Routing for deleting a user """

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    print(f"LOOK HERE: {User.query.all()}")
    return redirect("/users")


@app.route('/users/user/<int:id>/edit', methods=["POST", "GET"])
def edit(id):
    """Routing for editing a user"""

    user = User.query.get_or_404(id)

    if request.method == "POST":
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        img_url = request.form['img-url']
        img_url = img_url if img_url else None

        user.first_name = first_name
        user.last_name = last_name
        user.img_url = img_url
        db.session.commit()

        return redirect('/users')

    return render_template("edit.html", user=user)
