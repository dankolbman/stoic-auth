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
    @api.doc(responses={400: 'missing fields', 201: 'user registered'})
    def post(self, **kwargs):
        """
        Register a new user

        Create a new user:

        ```
        POST /user -d '
        {
            "username": "Jim",
            "password": "123",
            "email": "jim@example.com"
        }'
        ```
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
            return {'status': 'email taken'}, 400
        if (User.query.filter_by(username=fields['username']).first()
                is not None):
            return {'status': 'username taken'}, 400
        user = User(username=fields['username'],
                    password=fields['password'],
                    email=fields['email'],
                    active=True)
        db.session.add(user)
        db.session.commit()
        return {'username': user.username,
                'email': fields['email'],
                'status': 'user registered'}, 201


@api.route('/<string:username>')
class UserResource(Resource):
    @api.doc(responses={
                200: 'user found',
                404: 'user not found'})
    def get(self, username):
        """
        Get a user by username
        """
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return {'status': 'user found', 'user': user.to_json()}, 200

        return {'status': 'user not found'}, 404
