import json
import unittest
from datetime import datetime

from flask import current_app, url_for
from users import create_app, db
from users.model import User

from test.utils import make_user, api_headers


class AuthTestCase(unittest.TestCase):

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

    def _get_jwt(self):
        pass

    def test_jwt(self):
        """
        Test generation of JWT token
        """
        # create a user
        json_resp = make_user(self.client)
        resp = self.client.get('/auth/status',
                               headers=api_headers())
        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(json_resp['username'], 'not authenticated')
        # get a token
        resp = self.client.post('/auth',
                                headers=api_headers(),
                                data=json.dumps({'username': 'Dan',
                                                 'password': '123'}))
        json_resp = json.loads(resp.data.decode('utf-8'))
        # check status
        headers = api_headers()
        headers.update({'Authorization': "JWT " + json_resp['access_token']})
        resp = self.client.get('/auth/status',
                               headers=headers)
        json_resp = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(json_resp['username'], 'Dan')
