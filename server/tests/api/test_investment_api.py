from decimal import Decimal
import json
import mock
import os
from unittest import TestCase


import api
from business.database_table import DatabaseTableException
from business.user import UserException
import business.investment


MOCK_INVESTMENT_ENTRY = {
    'DateCreated': '2017-04-09',
    'InitialValue': Decimal('824.67'),
    'InvestmentID': 'ad2d884e-8a82-4a39-9548-00c86a674128',
    'ShareCount': Decimal('2'),
    'StockSymbol': 'goog',
    'UserID': 'exists'
}


class MockInvestment(object):
    def __init__(self):
        pass

    def get_investment(self, index_value):
        if index_value != 'exists':
            raise DatabaseTableException('No row with primary key value of "%s" exists.' % index_value)

        return MOCK_INVESTMENT_ENTRY

    def add_investment(self, user_id, stock_symbol, share_count, date_created, initial_investment_value):
        business.investment._validate_share_count(share_count)
        business.investment._validate_initial_investment_value(initial_investment_value)

    def remove_investment(self, index_value):
        if index_value != 'exists':
            raise DatabaseTableException('No row with primary key value of "%s" exists.' % index_value)
            
    def update_investment(self, index_value, share_count):
        if index_value != 'exists':
            raise DatabaseTableException('No row with primary key value of "%s" exists.' % index_value)
        
    def get_all_investments_of_user(self, index_value):
        if index_value != 'exists':
            raise DatabaseTableException('No row with primary key value of "%s" exists.' % index_value)
        
        return [
            MOCK_INVESTMENT_ENTRY
        ]
        
def mock_update_user_balance(user_id, value):
    if user_id != 'exists':
        raise DatabaseTableException('No row with primary key value of "%s" exists.' % user_id)
        
    if value == -100:
        raise UserException('Cannot spend this much currency')
        
def mock_get_stock_realtime(stock_symbol):
    if stock_symbol != 'exists':
        raise ValueError('')
        
    return {
        'stock_name': 'stock',
        'stock_open': '100',
        'stock_price': '100',
    }


class TestUnitInvestmentAPI(TestCase):        
    @mock.patch('business.investment.Investment', return_value=MockInvestment())
    def test_get_investment_nonexistant_user(self, mock_investment):
        with self.assertRaises(ValueError):
            api.get_investment('nonexistant')
            
    @mock.patch('business.investment.Investment', return_value=MockInvestment())
    def test_get_investment_happy_case(self, mock_investment):
        self.assertEquals(api.get_investment('exists'), MOCK_INVESTMENT_ENTRY)
        
    @mock.patch('business.investment.Investment', return_value=MockInvestment())
    def test_get_all_investments_of_user_nonexistant_user(self, mock_investment):
        with self.assertRaises(ValueError):
            api.get_all_investments_by_user('nonexistant')
        
    @mock.patch('business.investment.Investment', return_value=MockInvestment())
    def test_get_all_investments_of_user_happy_case(self, mock_investment):
        self.assertEquals(api.get_all_investments_by_user('exists'), [
            MOCK_INVESTMENT_ENTRY
        ])
        
    @mock.patch('business.investment.Investment', return_value=MockInvestment())
    @mock.patch('api.user_api.update_user_balance', side_effect=mock_update_user_balance)
    @mock.patch('api.stock_api.get_stock_realtime', side_effect=mock_get_stock_realtime)
    def test_create_investment_nonexistant_user(self, mock_investment, mock_update, mock_stock):
        with self.assertRaises(ValueError):
            api.create_investment('nonexistant', 'exists', 3)

    @mock.patch('business.investment.Investment', return_value=MockInvestment())
    @mock.patch('api.user_api.update_user_balance', side_effect=mock_update_user_balance)
    @mock.patch('api.stock_api.get_stock_realtime', side_effect=mock_get_stock_realtime)
    def test_create_investment_invalid_balance(self, mock_investment, mock_update, mock_stock):
        with self.assertRaises(ValueError):
            api.create_investment('exists', 'exists', 2)
        
    @mock.patch('business.investment.Investment', return_value=MockInvestment())
    @mock.patch('api.user_api.update_user_balance', side_effect=mock_update_user_balance)
    @mock.patch('api.stock_api.get_stock_realtime', side_effect=mock_get_stock_realtime)
    def test_sell_investment_nonexistant_user(self, mock_investment, mock_update, mock_stock):
        with self.assertRaises(ValueError):
            api.sell_investment('nonexistant', 3)

    @mock.patch('business.investment.Investment', return_value=MockInvestment())
    @mock.patch('api.user_api.update_user_balance', side_effect=mock_update_user_balance)
    @mock.patch('api.stock_api.get_stock_realtime', side_effect=mock_get_stock_realtime)
    def test_sell_investment_negative_share_count(self, mock_investment, mock_update, mock_stock):
        with self.assertRaises(ValueError):
            api.sell_investment('exists', -3)

    @mock.patch('business.investment.Investment', return_value=MockInvestment())
    @mock.patch('api.user_api.update_user_balance', side_effect=mock_update_user_balance)
    @mock.patch('api.stock_api.get_stock_realtime', side_effect=mock_get_stock_realtime)
    def test_sell_investment_excessive_share_count(self, mock_investment, mock_update, mock_stock):
        with self.assertRaises(ValueError):
            api.sell_investment('exists', 3)

    @mock.patch('business.investment.Investment', return_value=MockInvestment())
    @mock.patch('api.user_api.update_user_balance', side_effect=mock_update_user_balance)
    @mock.patch('api.stock_api.get_stock_realtime', side_effect=mock_get_stock_realtime)
    def test_sell_investment_happy_case_partial_sale(self, mock_investment, mock_update, mock_stock):
        api.sell_investment('exists', 1)

    @mock.patch('business.investment.Investment', return_value=MockInvestment())
    @mock.patch('api.user_api.update_user_balance', side_effect=mock_update_user_balance)
    @mock.patch('api.stock_api.get_stock_realtime', side_effect=mock_get_stock_realtime)
    def test_sell_investment_happy_case_entire_sale(self, mock_investment, mock_update, mock_stock):
        api.sell_investment('exists', 2)
    