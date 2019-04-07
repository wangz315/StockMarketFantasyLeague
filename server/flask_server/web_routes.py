import json


import flask


import api
import server


from flask import make_response


def assign_routes(app):
    @app.route('/')
    def home():
        return make_response(open('flask_server/templates/index.html').read())
            
    @app.errorhandler(404)
    def serve_error_page(error, error_code=500):
        code = error.code if hasattr(error, 'code') else error_code
        
        return make_response(open('flask_server/templates/index.html').read())
