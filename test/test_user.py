import json
import unittest
from datetime import datetime

from flask import current_app, url_for
from users import create_app, db
from users.model import User, Permission

from test.utils import FlaskTestCase, make_user, api_headers


class UserTestCase(FlaskTestCase):

    def test_new_user(self):
        """
        Test user creation via REST API
        """
        json_resp = make_user(self.client)
        # check api response
        self.assertEqual(json_resp['status'], 'user registered')
        self.assertEqual(json_resp['username'], 'Dan')
        # check that user is in database
        self.assertEqual(User.query.count(), 1)

        # check malformed query
        resp = self.client.post('/user/',
                                headers=api_headers(),
                                data=json.dumps({'username': 'Dan'}))
        json_resp = json.loads(resp.data.decode('utf-8'))
        # check api response
        self.assertEqual(resp.status, '400 BAD REQUEST')
        self.assertEqual(json_resp['status'], 'missing fields')
        self.assertEqual(json_resp['missing'], ['email', 'password'])

    def test_duplicate_user(self):
        """
        Test trying to register a duplicate user
        """
        json_resp = make_user(self.client)
        json_resp = make_user(self.client, username='Blah')
        # email should be taken
        self.assertEqual(json_resp['status'], 'email taken')
        # check only one user in the db
        self.assertEqual(User.query.count(), 1)
        # username should be taken
        json_resp = make_user(self.client, email='other@test.com')
        # check api response
        self.assertEqual(json_resp['status'], 'username taken')

    def test_user_by_username(self):
        """
        Test retrieving user by username
        """
        username = make_user(self.client)['username']
        resp = self.client.get('/user/'+username,
                               headers=api_headers())
        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(json_resp['status'], 'user found')
        self.assertEqual(json_resp['user']['username'], username)
