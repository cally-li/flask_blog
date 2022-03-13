
from flask import Blueprint, render_template

errors=Blueprint('errors', __name__)

#app_errorhandler makes the function active for entire app (not just this blueprint)
#since these are errors, we need to specify which response code to return for each function (default is 200)
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'),404

@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'),403

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'),500