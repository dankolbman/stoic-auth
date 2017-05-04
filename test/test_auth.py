import json
import jwt
import unittest
from datetime import datetime

from flask import current_app, url_for

from test.utils import FlaskTestCase, make_user, api_headers


class AuthTestCase(FlaskTestCase):

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

    def test_permissions(self):
        """
        Test the authorization permissions in the JWT
        """
        json_resp = make_user(self.client, 'test')
        # get a token
        resp = self.client.post('/auth',
                                headers=api_headers(),
                                data=json.dumps({'username': 'test',
                                                 'password': '123'}))
        json_resp = json.loads(resp.data.decode('utf-8'))['access_token']
        token = jwt.decode(json_resp, 'secret', algorithms=['HS256'])
        self.assertIn('permissions', token['identity'])
