from unittest import mock
import unittest

from Riki import app

from wiki.web.routes import user_create

class TestAdminPage(unittest.TestCase):
   
    def test_admin(self, mocked_render):
        self.assertEquals(user_create, 1)
