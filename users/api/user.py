from flask import request, jsonify, session
from ..model import User
from flask_restplus import Api, Resource, Namespace, fields
from .. import db


api = Namespace('user', description='User service')


@api.route('/status')
class Status(Resource):
    def get(self, **kwargs):
        return {'status': 200,
                'version': '1.0'}, 200


@api.route('/')
class NewUser(Resource):
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
        user = User(username=fields['username'],
                    password=fields['password'],
                    email=fields['password'],
                    active=True)
        db.session.add(user)
        db.session.commit()
        return {'username': user.username,
                'email': fields['email'],
                'status': 'user registered'}, 201

@api.route('/<string:username>')
class UserResource(Resource):
    def get(self, **kwargs):
        """
        Get a user by id
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
        user = User(username=fields['username'],
                    password=fields['password'],
                    email=fields['password'],
                    active=True)
        db.session.add(user)
        db.session.commit()
        return jsonify({'username': user.username,
                'email': fields['email'],
                'status': 'user registered'}), 201
