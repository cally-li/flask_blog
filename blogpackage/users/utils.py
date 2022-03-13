from distutils.command.config import config
import os
import secrets
import smtplib
import ssl
from email.message import EmailMessage

from blogpackage.config import Config
from flask import url_for, current_app
from PIL import Image


def save_picture(updated_pic):
    # rename user's submitted picture to avoid duplicate file names
    hex_name = secrets.token_hex(8)
    _, file_extension = os.path.splitext(updated_pic.filename)
    picture_name = hex_name + file_extension
    # define path where pic is saved. app.root_path = root directory of the app (blogpackage)
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_name)
    # resize picture with Pillow to prevent overcapicitating filesystem with large pictures
    thumbnail_size = (150, 150)
    i = Image.open(updated_pic)
    i.thumbnail(thumbnail_size)
    # save the picture to declared path
    i.save(picture_path)

    return picture_name


def send_reset_email(user):
    token = user.get_reset_pw_token()
    msg = EmailMessage()
    msg['Subject'] = 'Reset your Password'
    msg['From'] = Config.EMAIL_ADDRESS
    msg['To'] = user.email
    msg.set_content(f'''
        Hello {user.username},

        To reset your password, please visit the following link:
        {url_for('users.reset_password', token=token, _external=True)} 

        If you did not make this request, please ignore this email and no changes will be made. This link will expire in 10 minutes.
        ''')  # external=True : generate the full URL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
        smtp.send_message(msg)


