import json
from unittest import TestCase


import flask_server.server as server


class TestUnitGenerateErrorResponse(TestCase):
    def test_generate_error_response_none_parameter(self):
        with self.assertRaises(TypeError):
            server._generate_error_response(None)

    def test_generate_error_response_happy_case(self):
        error_json = json.loads(server._generate_error_response(ValueError('foo')))
        
        self.assertEquals(error_json['Error'], 'ValueError')
        self.assertEquals(error_json['Message'], 'foo')
        
        