from unittest import TestCase


import flask_server


class TestUnitWebRoutes(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = flask_server.app.test_client()
        cls.app.testing = True

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_homepage_happy_case(self):
        page_response = self.app.get('/')

        self.assertEquals(page_response.status_code, 200)