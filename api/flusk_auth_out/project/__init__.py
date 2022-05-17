from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from .auth import add_auth_method
from .main import add_main_method
from . import dbms

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://igor:i4127493I@192.168.5.157:5432/postgres"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    add_auth_method(api)
    add_main_method(api)
    return app
