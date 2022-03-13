from functools import wraps
from flask_login import current_user
from blogpackage.config import Config
from flask import (flash, redirect, url_for)

#decorator to restrict view access to admin
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.email==Config.EMAIL_ADDRESS:
            return func(*args, **kwargs)
        else:
            flash("You don't have permission to access this page.")
            return redirect(url_for('main.home'))
    return decorated_view