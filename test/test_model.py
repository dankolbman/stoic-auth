import json
import unittest

from flask import current_app, url_for
from test.utils import FlaskTestCase, make_user, api_headers
from users.model import User, Permission


class ModelTestCase(FlaskTestCase):

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_permissions(self):
        """
        Test user permissions
        """
        json_resp = make_user(self.client, 'Dan')
        user = User.query.filter_by(username='Dan').one()
        self.assertEqual(len(user.permissions), 2)
        perms = [p.name for p in user.permissions]
        self.assertIn('users_view_me', perms)
        self.assertIn('points_create', perms)
