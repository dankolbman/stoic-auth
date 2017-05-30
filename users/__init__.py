import subprocess
from datetime import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, _default_jwt_payload_handler
from config import config

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    # insert app permissions
    from .api import api
    api.init_app(app)
    from .api.auth import authenticate, identity
    jwt = JWT(app, authenticate, identity)

    @jwt.jwt_payload_handler
    def make_payload(identity):
        iat = datetime.utcnow()
        exp = iat + app.config.get('JWT_EXPIRATION_DELTA')
        nbf = iat + app.config.get('JWT_NOT_BEFORE_DELTA')
        perms = [p.name for p in identity.permissions]
        return {'exp': exp, 'iat': iat, 'nbf': nbf,
                'identity': {'username': identity.username,
                             'permissions': perms}}

    @app.route('/status')
    def status():
        return jsonify({
            "version": (subprocess.check_output(
                        ['git', 'rev-parse', '--short', 'HEAD'])
                        .decode('utf-8').strip()),
            "status": 200})

    return app
