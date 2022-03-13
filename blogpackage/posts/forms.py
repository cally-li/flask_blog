from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='Title required!')])
    content = TextAreaField('Content', validators=[DataRequired(message='Content required!')])
    submit = SubmitField('Post')


class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Name required!')])
    email = StringField('Email', validators=[
                        DataRequired(message='Email required!'), Email()])
    content = TextAreaField('Comment', validators=[DataRequired(message='Content required!')])
    submit = SubmitField('Comment')
