from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_moment import Moment
from flask_login import LoginManager
from flask_mail import Mail
import os
from .config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
moment = Moment()
mail = Mail()


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'
    
    from flaskblog.user.routes import users
    from flaskblog.post.routes import posts
    from flaskblog.main.routes import main
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    
    return app