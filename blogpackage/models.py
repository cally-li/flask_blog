from datetime import datetime
from time import time
from blogpackage import db, login_manager
from flask import current_app
from flask_login import UserMixin
import jwt


#define user_loader fxn- used to reload user object from user ID stored in the session (decorator lets the extension know to find your users by id with this function)
@login_manager.user_loader  
def load_user(user_id):
    return User.query.get(int(user_id))
#returns the user corresponding to the id

# define database structure
  #UserMixin provides default implementations for the methods that flask-login expects user objects to possess (provides 'is_authenticated', 'is_active', 'is_anonymous', and 'get_id' methods to the class )
class User(db.Model, UserMixin):
    # primary key uniquely defines each class instance
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # one-to-many relationship (several posts per user). define dependency b/w user and post - reference Post class as the arg
    posts = db.relationship('Post', backref='author', lazy=True)              
    def __repr__(self):
        return f'user ({self.username}, {self.email}, {self.image_file})'

    # define fxns to generate/verify JWT tokens for a user , payload is current user id
    #returns JWT token as a string
    def get_reset_pw_token(self, expires_sec=600):
        return jwt.encode(
            {'user_id': self.id, 'exp': time() + expires_sec}, 
            current_app.config['SECRET_KEY'],
            algorithm='HS256') 

    @staticmethod #instance (self variable) not passed in
    def verify_reset_pw_token(token):
        try: #try to validate token
            id_numb=jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])['user_id'] #extract user id as output
        except: #return none if exception raised (invalid token)
            return None
        return User.query.get(id_numb) #if no exception, return the user with the user id (value of 'user_id' key will be = the user's id )
            
        
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # calling datetime.utcnow() would incorrectly set default time = when app runs
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # one-to-many relationship: ForeignKey placed on child table - reference the table.column (user.id) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)              
    def __repr__(self):
        return f'Post ({self.title}, {self.date_posted})'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email= db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    def __repr__(self):
        comment_post= Post.query.get(self.post_id).title
        return f'Comment ("{self.content}", {self.email}, {self.date_posted}, Post: "{comment_post}")'
