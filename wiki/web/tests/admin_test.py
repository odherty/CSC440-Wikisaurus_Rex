from unittest import mock
import unittest


def mockRender(**args):
    returnValue = []
    for i in args:
        returnValue.append(i)

    return returnValue



class TestAdminPage(TestCase):

    @mock.patch('flask.render_template','mockRender')
    def test_user_create(mockRender):
        response = user_create()
        print(response)


     
