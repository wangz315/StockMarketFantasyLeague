from decimal import Decimal
import json
import mock
import os
from unittest import TestCase


from business.database_table import DatabaseTableException
import business.investment


PRIMARY_KEY = 'InvestmentID'


class MockDatabaseTable(object):
    def __init__(self):
        self.table_data = []
        self.reset_table_data()
        
    def reset_table_data(self):
        self.table_data = json.loads(open(os.path.join(os.path.dirname(__file__), 'investment_stub.json')).read())

    def _has_row(self, index_value):
        result = False
        
        for row in self.table_data:
            if row[PRIMARY_KEY] == index_value:
                result = True
                break

        return result
        
    def get_row(self, index_value):
        result = None

        for row in self.table_data:
            if row[PRIMARY_KEY] == index_value:
                result = row
                break

        if result is None:
            raise DatabaseTableException('No row with primary key value of "%s" exists.' % index_value)

        return result

    def put_row(self, **kwargs):
        if not kwargs.has_key(PRIMARY_KEY):
            raise DatabaseTableException('No Primary Key')
        elif self._has_row(kwargs[PRIMARY_KEY]):
            raise DatabaseTableException('Key already exists')

        self.table_data.append(kwargs)

    def delete_row(self, index_value):
        if not self._has_row(index_value):
            raise DatabaseTableException('No Primary Key')
            
        for row in self.table_data:
            if row[PRIMARY_KEY] == index_value:
                self.table_data.remove(row)
                break

    def update_row(self, index_value, **kwargs):
        row = self.get_row(index_value)

        if kwargs.has_key(PRIMARY_KEY):
            raise DatabaseTableException('Can\'t change primary key')

        row.update(kwargs)

    def get_all_rows(self):
        return self.table_data


class TestUnitInvestment(TestCase):
    @mock.patch('business.database_table.DatabaseTable', return_value=MockDatabaseTable())
    def setUp(self, mock_database_table):
        self.test_investment_table = business.investment.Investment()
        self.test_investment_table._investment_table.reset_table_data()

    def test_get_investment_nonexistant(self):
        with self.assertRaises(DatabaseTableException):
            self.test_investment_table.get_investment('nonexistant')

    def test_get_investment_happy_case(self):
        self.assertEquals(self.test_investment_table.get_investment('someInvestmentID')['UserID'], 'alpha1992')

    def test_add_investment_happy_case(self):
        test_investment_id = self.test_investment_table.add_investment('tomy2005', 'amzn', 4, '1990-4-19', Decimal('2031.34'))
        
        self.assertEquals(self.test_investment_table.get_investment(test_investment_id)['UserID'], 'tomy2005')
        
    def test_remove_investment_nonexistant(self):
        with self.assertRaises(DatabaseTableException):
            self.test_investment_table.remove_investment('nonexistant')

    def test_remove_investment_happy_case(self):
        self.test_investment_table.remove_investment('someInvestmentID')
        
        with self.assertRaises(DatabaseTableException):
            self.test_investment_table.get_investment('someInvestmentID')
    
    def test_update_investment_nonexistant(self):
        with self.assertRaises(DatabaseTableException):
            self.test_investment_table.update_investment('nonexistant', Decimal(3))

    def test_update_investment_happy_case(self):
        self.test_investment_table.update_investment('someInvestmentID', Decimal(10000))
        
        self.assertEquals(self.test_investment_table.get_investment('someInvestmentID')['ShareCount'], Decimal(10000))

    def test_get_all_investments_of_user_happy_case(self):
        self.assertEquals(self.test_investment_table.get_all_investments_of_user('alpha1992')[0][PRIMARY_KEY], 'someInvestmentID')
        
class TestUnitInvestmentValidators(TestCase):
    def test_validate_share_count_invalid_float_type(self):
        with self.assertRaises(business.investment.InvestmentException):
            business.investment._validate_share_count(0.0)
            
    def test_validate_share_count_negative_value(self):
        with self.assertRaises(business.investment.InvestmentException):
            business.investment._validate_share_count(-1)
            
    def test_validate_share_count_zero_shares(self):
        with self.assertRaises(business.investment.InvestmentException):
            business.investment._validate_share_count(0)
            
    def test_validate_share_count_happy_case(self):
        business.investment._validate_share_count(1)
            
    def test_validate_initial_investment_value_non_decimal_value(self):
        with self.assertRaises(business.investment.InvestmentException):
            business.investment._validate_initial_investment_value(-1)
            
    def test_validate_initial_investment_value_negative_value(self):
        with self.assertRaises(business.investment.InvestmentException):
            business.investment._validate_initial_investment_value(Decimal(-1))
            
    def test_validate_initial_investment_value_happy_case(self):
        business.investment._validate_initial_investment_value(Decimal(0))
            
    def test_generate_investment_id_happy_case(self):
        test_uuid = business.investment._generate_investment_id()
        
        self.assertTrue(isinstance(test_uuid, basestring))
        self.assertTrue(len(test_uuid) > 0)
        