from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from blogpackage.config import Config

db = SQLAlchemy()
bcrypt=Bcrypt()
login_manager= LoginManager()
#set login route (route function name or absolute URL) for when non-users try to access @login_required views
login_manager.login_view='users.login' 
#style 'Log in to access this page' message
login_manager.login_message_category='alert alert-warning' 

# app factory: define function to create different instances of the app with diff configs
#pass in the configuration object you want to use for your app
def create_app(config_class=Config):
    app = Flask(__name__)
    # app.config.from_pyfile(config_filename)
    app.config.from_object(config_class)

    #make admin email an available variable in all templates (for the layout.html template)
    @app.context_processor
    def inject_to_templates():
        return {'admin_email': Config.EMAIL_ADDRESS}

    #initialize objects by passing in app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    #since routes.py files imports 'app' from this init module, we import these files last to avoid circular imports
    #import blueprint instances
    from blogpackage.users.routes import users
    from blogpackage.posts.routes import posts
    from blogpackage.main.routes import main
    from blogpackage.errors.handlers import errors
    #register blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # leave extension objects outside of the function so that they're are not bound to a specific app ( no application-specific state is stored on the extension object, so one extension object can be used for multiple apps)
    # pass app to extensions
    return app