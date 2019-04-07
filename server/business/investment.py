import decimal
import numbers
import uuid


import database_table


INVESTMENT_TABLE_NAME = 'Investments'


class InvestmentException(Exception):
    pass


def _generate_investment_id():
    return str(uuid.uuid4())

def _validate_share_count(share_count):
    if isinstance(share_count, numbers.Integral) is False or share_count <= 0:
        raise InvestmentException('Invalid share count "%s". Should be an integer greater than 0.' % share_count)

def _validate_initial_investment_value(initial_investment_value):
    if isinstance(initial_investment_value, decimal.Decimal) is False or initial_investment_value < 0:
        raise InvestmentException('Initial investment value "%s" should be a number that is greater than or equal to 0.' % initial_investment_value)


class Investment(object):
    def __init__(self):
        self._investment_table = database_table.DatabaseTable(INVESTMENT_TABLE_NAME)
        
    def get_all_investments_of_user(self, user_id):
        investments = self._investment_table.get_all_rows()
        result = []

        for investment in investments:
            if investment['UserID'] == user_id:
                result.append(investment)
        
        return result

    def add_investment(self, user_id, stock_symbol, share_count, date_created, initial_investment_value):
        _validate_share_count(share_count)
        _validate_initial_investment_value(initial_investment_value)
        
        new_investment_id = _generate_investment_id()

        self._investment_table.put_row(
            InvestmentID=new_investment_id,
            UserID=user_id,
            StockSymbol=stock_symbol,
            ShareCount=share_count,
            InitialValue=initial_investment_value,
            DateCreated=date_created
        )
        
        return new_investment_id

    def get_investment(self, investment_id):
        return self._investment_table.get_row(investment_id)
        
    def remove_investment(self, investment_id):
        self._investment_table.delete_row(investment_id)
        
    def update_investment(self, investment_id, share_count):
        self._investment_table.update_row(investment_id, ShareCount=share_count)
