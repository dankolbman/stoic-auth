import json
import unittest
from users import create_app, db
from users.model import User, Permission


class FlaskTestCase(unittest.TestCase):
    """ Contains base logic for setting up a Flask app """

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        Permission.create_permissions()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


def api_headers():
    """
    Headers for json request
    """
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def make_user(client, username='Dan'):
    resp = client.post('/user/',
                       headers=api_headers(),
                       data=json.dumps({'username': username,
                                        'email': 'dan@localhost.com',
                                        'password': '123'}))
    json_resp = json.loads(resp.data.decode('utf-8'))
    return json_resp
