

import unittest, json
from Riki import app
from os import path, remove
import datetime
import os

from wiki.web import current_users, UserManager
from flask_login import current_user, login_user

from wiki.web.routes import related
from wiki.core import Wiki
from flask import Flask, current_app


class RelatedTest(unittest.TestCase):
    """
        Test cases for related route
    """
        
    with app.app_context():
        
        def test_getlistoftags(self):
            test = Wiki("test1")
            test.title = "tes1t"
            test.tags ="test"
            test.url = "test1"
            taglist = ["test1"]
            self.assertEqual(taglist, related(test.url))
