from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty ', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created ', category='success')
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user=current_user)


@views.route("/delete-post/<id>")
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist ", category='error')
    elif current_user.id != post.User.id:
        flash("you dont have permission to delete this post ", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted ", category="success")

    return redirect(url_for("views.home"))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Username does not exist ', category="error")
        return redirect(url_for("views.home"))

    posts = user.posts
    return render_template("user_posts.html", user=current_user, posts=posts, username=username)


@views.route("/create-comment/<post_id>", methods=['POST'])
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('comment empty!', category='error')
    else:
        post = Post.query.filter_by(id=post_id).first()

        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for("views.home"))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('comment not found ', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('you do not have permission to delete this comment', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))
