import unittest, json
from Riki import app
from os import path, remove
import datetime

from wiki.web import current_users, UserManager
from flask_login import current_user, login_user
from wiki.web.forms import UserForm
from wiki.web.routes import user_create


class AdminUserTest(unittest.TestCase):

    def setUp(self):
        self.user_mng = UserManager('../tests/')
        self.app = app.test_client()
        self.app.testing = True

     
    def test_givenEndpoint(self):
        result = self.app.get('/user/')
        self.assertEqual(result.status_code, 500)