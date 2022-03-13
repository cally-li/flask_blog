import os

from blogpackage import bcrypt, db
from blogpackage.models import User
from blogpackage.users.forms import (LoginForm, RequestResetForm,
                                     ResetPasswordForm, SubscribeForm,
                                     UpdateAccountForm)
from blogpackage.users.utils import save_picture, send_reset_email
from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import current_user, login_required, login_user, logout_user

users = Blueprint('users', __name__)


@users.route("/subscribe", methods=['GET', 'POST'])
def subscribe():
    if current_user.is_authenticated:  # redirect to homepage if user is already logged in
        return redirect(url_for('main.home'))
    form = SubscribeForm()
    if form.validate_on_submit():  # validates POST requests
        # hash the inputted password
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')  # decode to utf-8 outputs a string
        # create user and add to database
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # flash mssg fxn accepts 2 args: message ,category (bootstrap alert classes can be used here)
        flash(
            f'Account created for {form.username.data}! Thanks for subscribing!', 'alert alert-success')
        # redirect to homepage upon successful registration
        return redirect(url_for('users.login'))
    return render_template('subscribe.html', title='Subscribe', form=form)
# pass in RegistrationForm instance to have access to it in template


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Logged in as {form.email.data}.', 'alert alert-success')
            # retrieve value of the 'next' query parameter in the URL
            next_page = request.args.get('next')
            # return logged in user to the @login_required page they were trying to access (if the query string exists under the key 'next'). otherwise return to homepage
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please try again.', 'alert alert-danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/account", methods=['GET', 'POST'])
@login_required  # only logged in users can access this view
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # if appropriate picture file has been submitted
        if form.user_picture.data:
            # remove old profile pic if it's not default image
            if current_user.image_file != 'default.jpg':
                current_picture_path = os.path.join(
                    current_app.root_path, 'static/profile_pics', current_user.image_file)
                os.remove(current_picture_path)
            # save submitted pic and set as current profile pic
            picture_file = save_picture(form.user_picture.data)
            current_user.image_file = picture_file
        # update username and email in database
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'alert alert-success')
        # redirect to avoid post-get redirect pattern
        return redirect(url_for('users.account'))
    elif request.method == 'GET':  # default: populate username/email field with current user's credentials
        form.username.data = current_user.username
        form.email.data = current_user.email
    # define object to represent path of current profile pic (pass into template)
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)



@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/request_reset", methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            f'An email has been sent to {form.email.data} with a link to reset the password associated with the account.', 'alert alert-warning')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # returns the user corresponding to user_d within token
    user = User.verify_reset_pw_token(token)
    if user is None:  # if token invalid
        flash(f'Invalid or expired link/token.', 'alert alert-warning')
        return redirect(url_for('users.request_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():  # else if token valid
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated!', 'alert alert-success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', title='Reset Password', form=form)
