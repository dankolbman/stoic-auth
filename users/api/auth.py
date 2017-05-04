from flask import request, jsonify, current_app
from flask_restplus import Api, Resource, Namespace, fields
from flask_jwt import _jwt_required, current_identity, JWTError
from werkzeug.security import safe_str_cmp
from ..model import User

api = Namespace('auth', description='Authentication service')


@api.route('/status')
class Status(Resource):
    def get(self, **kwargs):
        """
        Returns username if a JWT is found, otherwise reports not authenticated
        """
        username = 'not authenticated'
        try:
            _jwt_required(current_app.config['JWT_DEFAULT_REALM'])
            username = current_identity.username
        finally:
            resp = {'status': 200, 'version': '1.0', 'username': username}
            return resp, 200


def authenticate(username, password):
    """
    Authenticates a user and returns the model object
    """
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        return user


def identity(payload):
    """
    Resolves a user from the JWT payload
    """
    username = payload['identity']['username']
    return User.query.filter_by(username=username).first()
