from flask import request, jsonify, session
from ..model import User
from flask_restplus import Api, Resource, Namespace, fields
from datetime import datetime
import dateutil.parser
from .. import db, user_db


api = Namespace('user', description='User service')


@api.route('/status')
class Status(Resource):
    def get(self, **kwargs):
        return {'status': 200, 'version': '1.0'}


@api.route('/users', methods = ['POST'])
class UserResource(Resource):
    def post(self, **kwargs):
        """
        Register a new user
        """
        missing = []
        fields = {}
        # Retrieve user properties from json
        for v in ['username', 'email', 'password']:
            fields[v] = request.json.get(v)
            if fields[v] is None:
                missing.append(v)

        if len(missing) > 0:
            return {'missing': missing, 'status': 'missing fields'}, 400
        if User.query.filter_by(email=fields['email']).first() is not None:
            return {'missing': missing, 'status': 'user exists'}, 400
        user = user_db.create_user(username=fields['username'],
                                   password=fields['password'],
                                   email=fields['password'])
        return { 'username': user.username,
                 'email': fields['email'],
                 'status': 'user registered' }, 201
