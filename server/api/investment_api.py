import datetime
from decimal import Decimal


from business import database_table
from business import investment
from business import user
import stock_api
import user_api


def get_investment(investment_id):
    try:
        table = investment.Investment()
        
        investment_row = table.get_investment(investment_id)
        
        investment_row['CurrentValue'] = _get_current_stock_value(investment_row['StockSymbol'])
    
        return investment_row
    except database_table.DatabaseTableException as database_exception:
        raise ValueError(database_exception.message)

def get_all_investments_by_user(user_id):
    try:
        table = investment.Investment()
        
        all_investments = table.get_all_investments_of_user(user_id)
        
        for user_investment in all_investments:
            user_investment['CurrentValue'] = _get_current_stock_value(user_investment['StockSymbol'])
    
        return all_investments
    except database_table.DatabaseTableException as database_exception:
        raise ValueError(database_exception.message)
        
def create_investment(user_id, stock_symbol, share_count):
    try:
        table = investment.Investment()
        
        initial_investment_value = _get_current_stock_value(stock_symbol)
        date_created = datetime.datetime.now().strftime('%Y-%m-%d')
        
        user_api.update_user_balance(user_id, Decimal(-1.0) * initial_investment_value)
        
        return {
            'InvestmentID': table.add_investment(user_id, stock_symbol, int(share_count), date_created, initial_investment_value)
        }
    except (investment.InvestmentException, database_table.DatabaseTableException, user.UserException) as exception:
        raise ValueError(exception.message)
        
def sell_investment(investment_id, share_sell_count):
    try:
        table = investment.Investment()
        share_sell_count = Decimal(share_sell_count)
        investment_row = get_investment(investment_id)
        
        if share_sell_count <= 0:
            raise ValueError('Share sell count "%s" must be larger than 0.' % share_sell_count)
        elif share_sell_count > investment_row['ShareCount']:
            raise ValueError('Share sell count "%d" must be less than or equal to the total share count "%d".' % (share_sell_count, investment_row['ShareCount']))
        
        selling_value = _get_current_stock_value(investment_row['StockSymbol']) * share_sell_count
        user_api.update_user_balance(investment_row['UserID'], selling_value)
        
        if share_sell_count == investment_row['ShareCount']:
            table.remove_investment(investment_id)
        else:
            table.update_investment(investment_id, investment_row['ShareCount'] - share_sell_count)

    except (investment.InvestmentException, database_table.DatabaseTableException) as exception:
        raise ValueError(exception.message)
        
def _get_current_stock_value(stock_symbol):
    current_investment_value = 0
    
    try:
        current_investment_value = Decimal(stock_api.get_stock_realtime(stock_symbol)['stock_price'])
    except ValueError:
        # Could not reach Yahoo server. Don't need to error, just return the investment info as is.
        pass
        
    return current_investment_value