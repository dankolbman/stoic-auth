from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    from .api import api
    api.init_app(app)
    from .api.auth import authenticate, identity
    jwt = JWT(app, authenticate, identity)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    return app
