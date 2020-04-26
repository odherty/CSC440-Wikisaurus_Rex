from unittest import mock
import unittest

from Riki import app

from wiki.web.routes import user_create

class TestAdminPage(unittest.TestCase):
   
   with app.app_context():
        @mock.patch('render_template', return_value=1)
        def test_admin(self, mocked_render):
            self.assertEquals(user_create, 1)
