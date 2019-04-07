import mock
from unittest import TestCase
import urllib2


import yahoo_finance


from api import stock_api


MOCK_HISTORICAL = [
    {
        'Volume': '2950600',
        'Symbol': 'amzn',
        'Adj_Close': '842.700012',
        'High': '842.809998',
        'Low': '832.820007',
        'Date': '2017-02-15',
        'Close': '842.700012',
        'Open': '834.00'
    }
]


class MockShare(object):
    def __init__(self, name, open, value, history):
        self.name = name
        self.open = open
        self.value = value
        self.history = history
    
    def get_name(self):
        return self.name
    
    def get_open(self):
        return self.open
    
    def get_price(self):
        return self.value

    def get_historical(self, date_start, date_end=None):
        return self.history


class TestUnitGetStockRealtime(TestCase):
    @mock.patch('yahoo_finance.Share')
    def test_get_stock_realtime_nonexistant_stock_symbol(self, mocked_share_class):
        mocked_share_class.return_value = MockShare(None, None, None, None)
        
        with self.assertRaises(ValueError):
            stock_api.get_stock_realtime('foo')
            
    @mock.patch('yahoo_finance.Share')
    def test_get_stock_realtime_happy_case(self, mocked_share_class):
        mocked_share_class.return_value = MockShare('foo', '0.1', '0.2', None)
        
        test_stock = stock_api.get_stock_realtime('foo')
        
        self.assertTrue(test_stock['stock_name'] == 'foo')
        self.assertTrue(test_stock['stock_open'] == '0.1')
        self.assertTrue(test_stock['stock_price'] == '0.2')
        
class TestUnitGetStockHistorical(TestCase):
    @mock.patch('yahoo_finance.Share')
    def test_get_stock_historical_nonexistant_stock_symbol(self, mocked_share_class):
        mocked_share_class.return_value = MockShare(None, None, None, None)
        
        with self.assertRaises(ValueError):
            stock_api.get_stock_historical('foo', '1992-08-27', date_end='1992-08-27')

    @mock.patch('yahoo_finance.Share')
    def test_get_stock_historical_happy_case_unspecified_date_end(self, mocked_share_class):
        mocked_share_class.return_value = MockShare('foo', '0.1', '0.2', MOCK_HISTORICAL)
        
        stock_history = stock_api.get_stock_historical('foo', '1992-08-27')
        
        self.assertEquals(str(MOCK_HISTORICAL), str(stock_history))

    @mock.patch('yahoo_finance.Share')
    def test_get_stock_historical_happy_case_specified_date_end(self, mocked_share_class):
        mocked_share_class.return_value = MockShare('foo', '0.1', '0.2', MOCK_HISTORICAL)
        
        stock_history = stock_api.get_stock_historical('foo', '1992-08-27', date_end='1992-08-27')
        
        self.assertEquals(str(MOCK_HISTORICAL), str(stock_history))

class TestUnitRetrieveYahooFinanceStockInfo(TestCase):
    @mock.patch('yahoo_finance.Share', side_effect=urllib2.HTTPError('url', 400, 'message', 'headers', None))
    def test_retrieve_yahoo_no_server_response(self, mocked_share_class):
        with self.assertRaises(ValueError):            
            stock_api._retrieve_yahoo_finance_stock_info('foo')

    @mock.patch('yahoo_finance.Share', side_effect=yahoo_finance.YQLResponseMalformedError())
    def test_retrieve_yahoo_malformed_server_error(self, mocked_share_class):
        with self.assertRaises(ValueError):            
            stock_api._retrieve_yahoo_finance_stock_info('!@')
    
    @mock.patch('yahoo_finance.Share')
    def test_retrieve_yahoo_happy_case(self, mocked_share_class):
        mock_share = MockShare('foo', '0.1', '0.2', None)
        mocked_share_class.return_value = mock_share
        
        self.assertTrue(stock_api._retrieve_yahoo_finance_stock_info('foo') is mock_share)

class TestUnitValidateISO8601DateFormat(TestCase):
    def test_validate_date_none_parameter(self):
        with self.assertRaises(TypeError):
            stock_api._validate_iso_8601_date_format(None)

    def test_validate_date_invalid_format(self):
        with self.assertRaises(ValueError):
            stock_api._validate_iso_8601_date_format('foo')

    def test_validate_date_happy_case(self):
        stock_api._validate_iso_8601_date_format('2003-07-21')