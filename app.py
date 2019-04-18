"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from models import db, connect_db, User, Post, Tag, PostTag
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
    return render_template('user.html', user=user, posts=posts)


@app.route('/users/user/<int:id>/delete')
def delete(id):
    """Routing for deleting a user """

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

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

        return redirect(f'/users/user/{id}')

    return render_template("create-post.html", id=id)


@app.route('/posts/<int:post_id>')
def post(post_id):
    """Views the post"""
    post = Post.query.get(post_id)
    return render_template("post.html", post=post)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Shows the form to edit a post """
    post = Post.query.get(post_id)
    return render_template('edit-post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
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


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Deletes a post given the id """

    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect("/users")


##################################################
# Tag stuff


@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_single_tag(tag_id):
    """Shows information about a tag """
    tag = Tag.query.get(tag_id)
    return render_template('tag-info.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """ Shows the edit form """
    tag = Tag.query.get(tag_id)
    return render_template('tag-edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """ Handles the edit submission"""
    print("Look here:, we've received a post request to edit", )
    tag = Tag.query.get(tag_id)

    # Grab the form info
    new_tag_name = request.form["tag-name"]

    # Edit
    tag.name = new_tag_name
    db.session.commit()

    return redirect(f'/tags/{tag_id}')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Deletes a tag_id given the id """

    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/users")


##################################################
# Refactoring
# It is better to separate get/post methods, because it is easier to understand
# Delete a tag has some bug - cascading
