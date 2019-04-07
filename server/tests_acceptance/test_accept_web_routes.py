from unittest import TestCase


import requests


import flask_server


class TestAcceptanceWebRoutes(TestCase):
    def test_get_homepage_happy_case(self):
        get_response = requests.get('http://localhost:5000')

        self.assertEquals(get_response.status_code, 200)