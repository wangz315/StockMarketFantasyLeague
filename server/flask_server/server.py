import json
import traceback


import flask


import api
import api_routes
import web_routes


app = flask.Flask(__name__)


api_routes.assign_routes(app)    
web_routes.assign_routes(app)
    
def run():
    print 'Starting server...'
    
    app.run(host='0.0.0.0', debug=True)
    
def _generate_error_response(exception):
    if issubclass(exception.__class__, Exception) is False:
        raise TypeError('Not an exception type.')
        
    return json.dumps({
        'Error': exception.__class__.__name__,
        'Message': exception.message,
        'Trace': traceback.format_exc()
    })