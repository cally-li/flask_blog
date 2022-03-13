from functools import wraps
from blogpackage import db
from blogpackage.models import Comment, Post
from blogpackage.posts.forms import CommentForm, PostForm
from blogpackage.config import Config
from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from blogpackage.posts.utils import admin_required

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
@admin_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'alert alert-success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='Create New Post')


# fetch a post by the post id
# add dynamic variable to URL with the format:<type:variable_name> (creates a variable in the URL that represents the post's id value)
@posts.route("/post/<int:post_id>",  methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)  # throw 404 error if not found
    post_comments = Comment.query.filter_by(
        post_id=post.id).order_by(Comment.date_posted.desc()).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(name=form.name.data, email=form.email.data,
                          content=form.content.data, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'alert alert-success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':  # default to populating name and email field with current user's credentials
        if current_user.is_authenticated: #if current user is logged in
            form.name.data = current_user.username
            form.email.data = current_user.email
    return render_template('post.html', title=post.title, post=post, form=form, post_comments=post_comments, admin_email=Config.EMAIL_ADDRESS)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # HTTP 403 Forbidden response if logged in user is not author of post
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'alert alert-success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':  # default to populating the title and content field with post title and content
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


# pressing 'Delete' button sends GET request to this route
@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'alert alert-success')
    return redirect(url_for('main.home'))


@posts.route("/post/<int:post_id>/<int:comment_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_comment(post_id, comment_id):
    post = Post.query.get_or_404(post_id)
    post_comment = Comment.query.get_or_404(comment_id)
    if current_user.email != Config.EMAIL_ADDRESS:
        abort(403)
    db.session.delete(post_comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'alert alert-success')
    return redirect(url_for('posts.post', post_id=post.id))
