"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from models import db, connect_db, User, Post
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

@app.route('/')
def root():
    """Homepage redirects to list of users."""

    return redirect("/users")

##################################################
# User route
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

        return redirect('/users')

    return render_template('create-user.html')


@app.route('/users/user/<int:id>')
def user(id):
    """Routing for viewing a user """

    user = User.query.get(id)
    posts = Post.query.filter(Post.user_id == id).all()
    print(f"~~~~~~ LOOK HERE:, i've got your posts: ", posts)
    return render_template('user.html', user=user, posts=posts)


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
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~ Edited")

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

##################################################
# Posting stuff

@app.route('/users/user/<int:id>/posts/new', methods=["POST", "GET"])
def new_post(id):
    """Route for making a new post"""
    if request.method == "POST":
        title = request.form['post-title']
        content = request.form['post-content']
        post = Post(title=title, content=content, user_id=id)
        db.session.add(post)
        db.session.commit()
        print("LOOK HERE: I added: ", post)

        return redirect(f'/users/user/{id}')
    
    return render_template("create-post.html", id=id)

@app.route('/posts/<int:post_id>')
def post(post_id):
    """Views the post"""
    post = Post.query.get(post_id)
    print("LOOK HERE: ", post)
    return render_template("post.html", post=post)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Shows the form to edit a post """

    post = Post.query.get(post_id)
    return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>', methods=["POST"])
def post_edit(post_id):
    """Shows the form to edit a post """

    # Grab the modified changes
    title = request.form['post-title']
    content = request.form['post-content']

    # Modify the post 
    post = Post.query.get(post_id)
    post.title = title
    post.content = content

    db.session.commit()

    return redirect(f'/posts/{post_id}')
  
##################################################
# Refactoring
#It is better to separate get/post methods, because it is easier to understand
# remove all prints