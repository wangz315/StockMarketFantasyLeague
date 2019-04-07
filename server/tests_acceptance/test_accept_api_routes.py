import requests
from unittest import TestCase
import uuid


import flask_server


def _is_error_response(response_json):
    return response_json.has_key('Message') and response_json.has_key('Trace') and response_json.has_key('Error') and (response_json['Error'] == 'ValueError' or response_json['Error'] == 'KeyError')

def _generate_random_user_id():
    return 'test-' + str(uuid.uuid1())[:10]


class TestAcceptanceAPIRoutes(TestCase):        
    def test_get_stock_realtime_nonexistant_stock_symbol(self):
        get_response = requests.get('http://localhost:5000/api/stock/nonexistant_stock_symbol')

        self.assertTrue(_is_error_response(get_response.json()))
        
    def test_get_stock_realtime_happy_case(self):
        response_json = requests.get('http://localhost:5000/api/stock/amzn').json()
        
        self.assertTrue(response_json.has_key('stock_name'))
        self.assertTrue(response_json.has_key('stock_open'))
        self.assertTrue(response_json.has_key('stock_price'))
        
    def test_get_stock_historical_missing_required_date_start(self):
        get_response = requests.get('http://localhost:5000/api/stock/nonexistant_stock_symbol/history')

        self.assertTrue(_is_error_response(get_response.json()))
        
    def test_get_stock_historical_invalid_date_start_format(self):
        get_response = requests.get('http://localhost:5000/api/stock/amzn/history', headers={
            'dateStart': 'foo'
        })

        self.assertTrue(_is_error_response(get_response.json()))
        
    def test_get_stock_historical_invalid_date_start(self):
        get_response = requests.get('http://localhost:5000/api/stock/amzn/history', headers={
            'dateStart': '2097-05-12'
        })

        self.assertTrue(_is_error_response(get_response.json()))
        
    def test_get_stock_historical_nonexistant_stock_symbol(self):
        get_response = requests.get('http://localhost:5000/api/stock/nonexistant_stock_symbol/history', headers={
            'dateStart': '2000-09-09'
        })

        self.assertTrue(_is_error_response(get_response.json()))

    def test_get_stock_historical_invalid_date_end_format(self):
        get_response = requests.get('http://localhost:5000/api/stock/amzn/history', headers={
            'dateStart': '2000-09-09',
            'dateEnd': 'foo'
        })

        self.assertTrue(_is_error_response(get_response.json()))

    def test_get_stock_historical_invalid_date_end(self):
        get_response = requests.get('http://localhost:5000/api/stock/amzn/history', headers={
            'dateStart': '2000-09-09',
            'dateEnd': '2000-07-01'
        })

        self.assertTrue(_is_error_response(get_response.json()))

    def test_get_stock_historical_happy_case(self):
        response_json = requests.get('http://localhost:5000/api/stock/amzn/history', headers={
            'dateStart': '2010-09-09',
            'dateEnd': '2010-09-10'
        }).json()
        
        self.assertTrue(response_json[0].has_key('Volume'))
        self.assertTrue(response_json[0].has_key('Symbol'))
        self.assertTrue(response_json[0].has_key('Adj_Close'))
        self.assertTrue(response_json[0].has_key('High'))
        self.assertTrue(response_json[0].has_key('Low'))
        self.assertTrue(response_json[0].has_key('Date'))
        self.assertTrue(response_json[0].has_key('Close'))
        self.assertTrue(response_json[0].has_key('Open'))
        
    def test_get_user_by_id_nonexistant_user(self):
        get_response = requests.get('http://localhost:5000/api/user/a')

        self.assertTrue(_is_error_response(get_response.json()))
        
    def test_get_user_by_id_happy_case(self):
        response_json = requests.get('http://localhost:5000/api/user/ostrich').json()
        
        self.assertEquals(response_json['UserID'], 'ostrich')
        self.assertTrue(response_json.has_key('Balance'))
        self.assertTrue(response_json.has_key('FirstName'))
        self.assertTrue(response_json.has_key('LastName'))
        
    def test_get_all_users_happy_case(self):
        response_json = requests.get('http://localhost:5000/api/user/').json()
        
        self.assertTrue(response_json[0].has_key('UserID'))
        self.assertTrue(response_json[0].has_key('Balance'))
        self.assertTrue(response_json[0].has_key('FirstName'))
        self.assertTrue(response_json[0].has_key('LastName'))
        
    def test_add_user_missing_header(self):
        post_response = requests.post('http://localhost:5000/api/user/', headers={})

        self.assertTrue(_is_error_response(post_response.json()))

    def test_add_user_invalid_user_id(self):
        post_response = requests.post('http://localhost:5000/api/user/', headers={
            'UserID': '',
            'FirstName': 'firstname',
            'LastName': 'lastname',
        })

        self.assertTrue(_is_error_response(post_response.json()))
        
    def test_add_user_invalid_first_name(self):
        post_response = requests.post('http://localhost:5000/api/user/', headers={
            'UserID': 'testtest',
            'FirstName': '',
            'LastName': 'lastname',
        })

        self.assertTrue(_is_error_response(post_response.json()))
        
    def test_add_user_invalid_last_name(self):
        post_response = requests.post('http://localhost:5000/api/user/', headers={
            'UserID': 'testtest',
            'FirstName': 'firstname',
            'LastName': '',
        })

        self.assertTrue(_is_error_response(post_response.json()))

    def test_add_user_happy_case(self):
        post_response = requests.post('http://localhost:5000/api/user/', headers={
            'UserID': _generate_random_user_id(),
            'FirstName': 'test_name',
            'LastName': 'test_name',
        })

        self.assertEquals(post_response.status_code, 200)
        self.assertEquals(post_response.text, '')
        
    def test_get_investment_nonexistant_investment_id(self):
        get_response = requests.get('http://localhost:5000/api/invest/a')

        self.assertTrue(_is_error_response(get_response.json()))

    def test_get_investment_happy_case(self):
        get_response = requests.get('http://localhost:5000/api/invest/do_not_delete_test_investment')
        response_json = get_response.json()
        
        self.assertEquals(response_json['UserID'], 'ostrich')
        self.assertTrue(response_json.has_key('DateCreated'))
        self.assertTrue(response_json.has_key('InitialValue'))
        self.assertTrue(response_json.has_key('InvestmentID'))
        self.assertTrue(response_json.has_key('StockSymbol'))
        self.assertTrue(response_json.has_key('ShareCount'))
        
    def test_get_all_investments_by_user_nonexistant_user(self):
        get_response = requests.get('http://localhost:5000/api/invest/getAll/a')

        self.assertEquals(len(get_response.json()), 0)
    
    def test_get_all_investments_by_user_happy_case(self):
        get_response = requests.get('http://localhost:5000/api/invest/getAll/ostrich')
        response_json = get_response.json()

        self.assertEquals(response_json[0]['UserID'], 'ostrich')
        self.assertTrue(response_json[0].has_key('DateCreated'))
        self.assertTrue(response_json[0].has_key('InitialValue'))
        self.assertTrue(response_json[0].has_key('InvestmentID'))
        self.assertTrue(response_json[0].has_key('StockSymbol'))
        self.assertTrue(response_json[0].has_key('ShareCount'))
        
    def test_create_investment_missing_header(self):
        post_response = requests.post('http://localhost:5000/api/invest/buy/', headers={})

        self.assertTrue(_is_error_response(post_response.json()))

    def test_create_investment_nonexistant_user_id(self):
        post_response = requests.post('http://localhost:5000/api/invest/buy/', headers={
            'UserID': 'a',
            'StockSymbol': 'amzn',
            'ShareCount': '3'
        })

        self.assertTrue(_is_error_response(post_response.json()))
        
    def test_create_investment_invalid_share_count(self):
        post_response = requests.post('http://localhost:5000/api/invest/buy/', headers={
            'UserID': 'ostrich',
            'StockSymbol': 'amzn',
            'ShareCount': '-3'
        })

        self.assertTrue(_is_error_response(post_response.json()))

    def test_create_investment_happy_case(self):
        post_response = requests.post('http://localhost:5000/api/invest/buy/', headers={
            'UserID': 'ostrich',
            'StockSymbol': 'tsn',
            'ShareCount': '1'
        })
        
        response_json = post_response.json()
        
        self.assertTrue(response_json.has_key('InvestmentID'))
        test_investment_id = response_json['InvestmentID']
        
        get_response = requests.get('http://localhost:5000/api/invest/' + test_investment_id)
        response_json = get_response.json()
        
        self.assertEquals(response_json['UserID'], 'ostrich')
        self.assertTrue(response_json.has_key('DateCreated'))
        self.assertTrue(response_json.has_key('InitialValue'))
        self.assertTrue(response_json.has_key('InvestmentID'))
        self.assertEquals(response_json['StockSymbol'], 'tsn')
        self.assertEquals(response_json['ShareCount'], 1)
        
    def test_sell_investment_missing_header(self):
        post_response = requests.post('http://localhost:5000/api/invest/sell/', headers={})

        self.assertTrue(_is_error_response(post_response.json()))

    def test_sell_investment_nonexistant_investment(self):
        post_response = requests.post('http://localhost:5000/api/invest/sell/', headers={
            'InvestmentID': '-',
            'ShareCount': '1',
        })

        self.assertTrue(_is_error_response(post_response.json()))
        
    def test_sell_investment_invalid_share_count(self):
        post_response = requests.post('http://localhost:5000/api/invest/sell/', headers={
            'InvestmentID': 'do_not_delete_test_investment',
            'ShareCount': '0',
        })

        self.assertTrue(_is_error_response(post_response.json()))
        
    def test_sell_investment_share_count_too_high(self):
        post_response = requests.post('http://localhost:5000/api/invest/sell/', headers={
            'InvestmentID': 'do_not_delete_test_investment_2',
            'ShareCount': '100',
        })

        self.assertTrue(_is_error_response(post_response.json()))
        
    def test_sell_investment_happy_case(self):
        initial_test_investment_state = requests.get('http://localhost:5000/api/invest/do_not_delete_test_investment').json()
    
        post_response = requests.post('http://localhost:5000/api/invest/sell/', headers={
            'InvestmentID': 'do_not_delete_test_investment',
            'ShareCount': '1',
        })
        
        final_test_investment_state = requests.get('http://localhost:5000/api/invest/do_not_delete_test_investment').json()

        self.assertEquals(post_response.status_code, 200)
        self.assertEquals(post_response.text, '')
        self.assertEquals(initial_test_investment_state['ShareCount'] - 1, final_test_investment_state['ShareCount'])