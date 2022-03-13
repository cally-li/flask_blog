import os

class Config:
    # set secret key for csrf and password reset (JWT) token 
    SECRET_KEY = os.environ.get('SECRET_KEY')  
    # set SQLite database location. /// is relative path; site.db database will be stored within same directory
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  
    EMAIL_ADDRESS=os.environ.get('GMAIL_USER')  
    EMAIL_PASSWORD=os.environ.get('GMAIL_PASS')  