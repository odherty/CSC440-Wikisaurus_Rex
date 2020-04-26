"""
user_profile_test.py
Author: Patrick O'Doherty
CSC440
"""

import unittest, json
from Riki import app
from os import path, remove
import datetime

from wiki.web import current_users, UserManager
from flask_login import current_user, login_user
from wiki.web.forms import UserUpdateForm
from wiki.web.routes import user_profile


class MyUserProfileTest(unittest.TestCase):
    """
        Test cases for user profile
    """

    def setUp(self):
        self.user_mng = UserManager('../tests/')
        self.app = app.test_client()
        self.app.testing = True

    def test_givenUser_whenChangePassword_thenJsonUpdates(self):
        user = self.user_mng.get_user("name")
        old_password = user.get('password')
        user.set('password', '123')
        self.assertEqual('123', user.get('password'))
        user.set('password', old_password)

    def test_givenUser_whenChangeEmail_thenJsonUpdates(self):
        user = self.user_mng.get_user("name")
        old_email = user.get('email')
        user.set('email', 'new_email@email.com')
        self.assertEqual('new_email@email.com', user.get('email'))
        user.set('email', old_email)

    def test_givenEndpoint_whenGET_thenReturns(self):
        result = self.app.get('/user/name/')
        self.assertEqual(result.status_code, 302)
