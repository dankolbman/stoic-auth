import json
import unittest
from datetime import datetime

from flask import current_app, url_for
from users import create_app, db
from users.model import User


class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _api_headers(self):
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_new_user(self):
        """
        Test user creation
        """
        resp = self.client.post('/user/users',
                                headers=self._api_headers(),
                                data=json.dumps({'username': 'Dan',
                                                 'email': 'dan@localhost.com',
                                                 'password': '123'}))
        json_resp = json.loads(resp.data.decode('utf-8'))
        # check api response
        self.assertEqual(resp.status, '201 CREATED')
        self.assertEqual(json_resp['username'], 'Dan')
        # check that user is in database
        self.assertEqual(User.query.count(), 1)

        # check malformed query
        resp = self.client.post('/user/users',
                                headers=self._api_headers(),
                                data=json.dumps({'username': 'Dan'}))
        json_resp = json.loads(resp.data.decode('utf-8'))
        # check api response
        self.assertEqual(resp.status, '400 BAD REQUEST')
        self.assertEqual(json_resp['status'], 'missing fields')
        self.assertEqual(json_resp['missing'], ['email', 'password'])

    def test_jwt(self):
        resp = self.client.get('/auth/status',
                               headers=self._api_headers())
        json_resp = json.loads(resp.data.decode('utf-8'))
        # create a user
        resp = self.client.post('/user/users',
                                headers=self._api_headers(),
                                data=json.dumps({'username': 'Dan',
                                                 'email': 'dan@localhost.com',
                                                 'password': '123'}))
        json_resp = json.loads(resp.data.decode('utf-8'))
        # get a token
        resp = self.client.post('/auth',
                                headers=self._api_headers(),
                                data=json.dumps({'username': 'Dan',
                                                 'password': '123'}))
        json_resp = json.loads(resp.data.decode('utf-8'))
        # check status
        headers = self._api_headers()
        headers.update({'Authorization': "JWT " + json_resp['access_token']})
        resp = self.client.get('/auth/status',
                               headers=headers)
        json_resp = json.loads(resp.data.decode('utf-8'))
