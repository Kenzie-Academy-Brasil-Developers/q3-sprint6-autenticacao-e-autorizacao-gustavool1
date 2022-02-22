
from app.configs import database, migration, jwt_auth
from flask import Flask
from app import routes
import os


def create_app():

    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['JSON_SORT_KEYS'] = False

    database.init_app(app)
    migration.init_app(app)

    jwt_auth.init_app(app)
    routes.init_app(app) 

    return app