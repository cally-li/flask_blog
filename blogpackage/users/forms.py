from blogpackage.models import User
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


# form class and its fields inherits from FlaskForm class
class SubscribeForm(FlaskForm):
    # form fields
    # validators check the limits in the field
    username = StringField('Username', validators=[
                           DataRequired(message='Username required'), Length(min=3, max=20, message='Username must be 3-20 characters.')])
    email = StringField('Email', validators=[
                        DataRequired(message='Email required'), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(message='Password required')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(message='Password confirmation required'), EqualTo('password')])
    submit = SubmitField('Subscribe')
    #catch errors for repeated username and email input
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken. Please choose another one.')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('There is already an account associated with this email.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(message='Email required'), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(message='Password required')])
    remember = BooleanField('Remember Me')
    login = SubmitField('Login')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError('There is no account associated with this email.')


class UpdateAccountForm(FlaskForm):

    username = StringField('Username', validators=[
                           DataRequired(message='Username required'), Length(min=3, max=20, message='Username must be 3-20 characters.')])
    email = StringField('Email', validators=[
                        DataRequired(message='Email required'), Email()])
    user_picture= FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'], 'Only .jpg and .png files are accepted.')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data!= current_user.username: #only perform validataion if user enters into the form a username that is not the current one
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username taken. Please choose another one.')
        else:
            return('You are already using this username.')

    def validate_email(self, email):
        if email.data!= current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('There is already an account associated with this email.')
        else:
            return('You are already using this email.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(message='Email required!'), Email()])
    submit = SubmitField('Send Link to Email')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError('There is no account associated with this email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
                             DataRequired(message='Password required')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(message='Password confirmation required'), EqualTo('password')])
    submit = SubmitField('Reset Password')
    