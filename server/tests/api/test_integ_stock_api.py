import datetime
from unittest import TestCase


from api import get_stock_realtime, get_stock_historical


DATE_START = '2014-01-01'
DATE_END = '2014-01-02'


class TestIntegrationGetStockRealtime(TestCase):
    def test_get_stock_realtime_none_stock_symbol(self):
        with self.assertRaises(ValueError):
            get_stock_realtime(None)
    
    def test_get_stock_realtime_malformed_stock_symbol(self):
        with self.assertRaises(ValueError):
            get_stock_realtime('!@')
            
    def test_get_stock_realtime_nonexistant_stock_symbol(self):
        with self.assertRaises(ValueError):
            get_stock_realtime('foo')
            
    def test_get_stock_realtime_happy_case(self):
        test_stock = get_stock_realtime('amzn')
        
        self.assertTrue(test_stock['stock_name'] == 'Amazon.com, Inc.')
        self.assertTrue(_is_float(test_stock['stock_open']))
        self.assertTrue(_is_float(test_stock['stock_price']))
        
class TestIntegrationGetStockHistorical(TestCase):
    def test_get_stock_historical_none_stock_symbol(self):
        with self.assertRaises(ValueError):
            get_stock_historical(None, DATE_START)
    
    def test_get_stock_historical_malformed_stock_symbol(self):
        with self.assertRaises(ValueError):
            get_stock_historical('!@', DATE_START)
            
    def test_get_stock_historical_nonexistant_stock_symbol(self):
        with self.assertRaises(ValueError):
            get_stock_historical('foo', DATE_START)
            
    def test_get_stock_historical_out_of_order_dates_specified(self):
        with self.assertRaises(ValueError):
            get_stock_historical('amzn', DATE_END, date_end=DATE_START)
            
    def test_get_stock_historical_happy_case(self):
        stock_history = get_stock_historical('amzn', DATE_START, DATE_END)
        history_entry = stock_history[0]
        
        self.assertTrue(len(stock_history) == 1)
        self.assertEquals(history_entry['Symbol'], 'amzn')
        self.assertTrue(_is_iso_8601_date_format(history_entry['Date']))
        
        self.assertTrue(_is_float(history_entry['Volume']))
        self.assertTrue(_is_float(history_entry['Adj_Close']))
        self.assertTrue(_is_float(history_entry['High']))
        self.assertTrue(_is_float(history_entry['Low']))
        self.assertTrue(_is_float(history_entry['Close']))
        self.assertTrue(_is_float(history_entry['Open']))
        
def _is_float(str):
    try:
        float(str)
        
        return True
    except ValueError:
        return False
        
def _is_iso_8601_date_format(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        
        return True
    except ValueError:
        return False