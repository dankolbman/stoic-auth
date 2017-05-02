from flask import request, jsonify
from flask_restplus import Api, Resource, Namespace, fields
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from ..model import User

api = Namespace('auth', description='Authentication service')


@api.route('/status')
class Status(Resource):
    def get(self, **kwargs):
        return {'status': 200,
                'version': '1.0'}

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
    user_id = payload['identity']
    return User.query.get_or_404(user_id)
