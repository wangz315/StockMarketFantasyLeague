import flask
import simplejson as json


import api
import server

API_RESPONSE_HEADER = {
    'Content-Type': 'application/json'
}


def assign_routes(app):
    @app.route('/api/stock/<string:stock_symbol>', methods=['GET'])
    def get_stock_realtime(stock_symbol):
        try:
            stock_data = api.get_stock_realtime(stock_symbol)

            return json.dumps(stock_data), 200, API_RESPONSE_HEADER
        except ValueError as value_error:
            return server._generate_error_response(value_error), 400, API_RESPONSE_HEADER
        except Exception as exception:
            return server._generate_error_response(exception), 500, API_RESPONSE_HEADER

    @app.route('/api/stock/<string:stock_symbol>/history', methods=['GET'])
    def get_stock_historical(stock_symbol):
        try:
            date_start = flask.request.headers['dateStart']
            date_end = flask.request.headers['dateEnd'] if 'dateEnd' in flask.request.headers else None
            stock_data = api.get_stock_historical(stock_symbol, date_start, date_end=date_end)

            return json.dumps(stock_data), 200, API_RESPONSE_HEADER
        except (ValueError, KeyError) as input_error:
            return server._generate_error_response(input_error), 400, API_RESPONSE_HEADER
        except Exception as exception:
            return server._generate_error_response(exception), 500, API_RESPONSE_HEADER

    @app.route('/api/user/<string:user_id>', methods=['GET'])
    def get_user_by_id(user_id):
        try:
            return json.dumps(api.get_user(user_id)), 200, API_RESPONSE_HEADER
        except ValueError as input_error:
            return server._generate_error_response(input_error), 400, API_RESPONSE_HEADER
        except Exception as exception:
            return server._generate_error_response(exception), 500, API_RESPONSE_HEADER

    @app.route('/api/user/', methods=['GET'])
    def get_all_users():
        try:
            return json.dumps(api.get_all_users()), 200, API_RESPONSE_HEADER
        except ValueError as input_error:
            return server._generate_error_response(input_error), 400, API_RESPONSE_HEADER
        except Exception as exception:
            return server._generate_error_response(exception), 500, API_RESPONSE_HEADER

    @app.route('/api/user/', methods=['POST'])
    def add_user():
        try:
            user_id = flask.request.headers['UserID']
            first_name = flask.request.headers['FirstName']
            last_name = flask.request.headers['LastName']

            api.add_user(user_id, first_name, last_name)
            
            return '', 200, API_RESPONSE_HEADER
        except (ValueError, KeyError) as input_error:            
            return server._generate_error_response(input_error), 400, API_RESPONSE_HEADER
        except Exception as exception:
            return server._generate_error_response(exception), 500, API_RESPONSE_HEADER

    @app.route('/api/invest/<string:investment_id>', methods=['GET'])
    def get_investment_by_id(investment_id):
        try:
            return json.dumps(api.get_investment(investment_id)), 200, API_RESPONSE_HEADER
        except ValueError as input_error:            
            return server._generate_error_response(input_error), 400, API_RESPONSE_HEADER
        except Exception as exception:
            return server._generate_error_response(exception), 500, API_RESPONSE_HEADER
            
    @app.route('/api/invest/getAll/<string:user_id>', methods=['GET'])
    def get_all_investments_by_user(user_id):
        try:
            return json.dumps(api.get_all_investments_by_user(user_id)), 200, API_RESPONSE_HEADER
        except ValueError as input_error:            
            return server._generate_error_response(input_error), 400, API_RESPONSE_HEADER
        except Exception as exception:
            return server._generate_error_response(exception), 500, API_RESPONSE_HEADER

    @app.route('/api/invest/buy/', methods=['POST'])
    def create_new_investment():
        try:
            user_id = flask.request.headers['UserID']
            stock_symbol = flask.request.headers['StockSymbol']
            share_count = flask.request.headers['ShareCount']
            
            return json.dumps(api.create_investment(user_id, stock_symbol, share_count)), 200, API_RESPONSE_HEADER
        except (ValueError, KeyError) as input_error:            
            return server._generate_error_response(input_error), 400, API_RESPONSE_HEADER
        except Exception as exception:
            return server._generate_error_response(exception), 500, API_RESPONSE_HEADER
            
    @app.route('/api/invest/sell/', methods=['POST'])
    def sell_existing_investment():
        try:
            investment_id = flask.request.headers['InvestmentID']
            share_count = flask.request.headers['ShareCount']
            
            api.sell_investment(investment_id, share_count)
            
            return '', 200, API_RESPONSE_HEADER
        except (ValueError, KeyError) as input_error:            
            return server._generate_error_response(input_error), 400, API_RESPONSE_HEADER
        except Exception as exception:
            return server._generate_error_response(exception), 500, API_RESPONSE_HEADER
