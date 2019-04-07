import datetime
import urllib2
import time


import yahoo_finance


RETRY_TIMER = 0.33
MAX_ATTEMPTS = 3


def get_stock_realtime(stock_symbol):
    stock = _retrieve_yahoo_finance_stock_info(stock_symbol)

    return {
        'stock_name': stock.get_name(),
        'stock_open': stock.get_open(),
        'stock_price': stock.get_price()
    }
    
def get_stock_historical(stock_symbol, date_start, date_end=None):
    stock = _retrieve_yahoo_finance_stock_info(stock_symbol)
    
    date_end = datetime.datetime.now().strftime('%Y-%m-%d') if date_end is None else date_end
    
    _validate_iso_8601_date_format(date_start)
    _validate_iso_8601_date_format(date_end)

    return stock.get_historical(date_start, date_end)

def _retrieve_yahoo_finance_stock_info(stock_symbol):
    try:
        stock = None
        
        for i in range(0, MAX_ATTEMPTS):
            try:
                stock = yahoo_finance.Share(stock_symbol)
                
                break
            except urllib2.HTTPError as http_error:
                time.sleep(RETRY_TIMER)
                    
        if stock is None:
            raise ValueError('Could not retrieve stock information for symbol "%s".' % stock_symbol)
        elif stock.get_name() is None:
            raise ValueError('No stock with symbol "%s" exists.' % stock_symbol)
        
        return stock
    except yahoo_finance.YQLResponseMalformedError as e:
        raise ValueError('Malformed stock symbol "%s".' % stock_symbol)
    
def _validate_iso_8601_date_format(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise 