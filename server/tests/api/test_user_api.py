import json
import mock
import os
from unittest import TestCase


import api
from business.database_table import DatabaseTableException
import business.user


MOCK_USER_ENTRY = {
    'UserID': 'foo',
    'FirstName': 'foo',
    'LastName': 'foo',
    'Balance': 0,
}


class MockUser(object):
    def __init__(self):
        pass

    def get_user(self, index_value):
        if index_value != 'exists':
            raise DatabaseTableException('No row with primary key value of "%s" exists.' % index_value)

        return MOCK_USER_ENTRY
        
    def put_user(self, index_value, first_name, last_name):
        if index_value == 'exists':
            raise DatabaseTableException('"%s" already exists.' % index_value)
        
        business.user._check_user_id(index_value)
        business.user._check_name(first_name)
        business.user._check_name(last_name)
        
    def update_user_balance(self, user_id, balance_update_amount):
        if user_id != 'exists':
            raise DatabaseTableException('No row with primary key value of "%s" exists.' % user_id)
        
        business.user._check_balance(balance_update_amount)
        
    def get_all_users(self):
        return {
            MOCK_USER_ENTRY['UserID']: MOCK_USER_ENTRY
        }


class TestUnitUser(TestCase):        
    @mock.patch('business.user.User', return_value=MockUser())
    def test_get_user_nonexistant_user(self, mock_user):
        with self.assertRaises(ValueError):
            api.get_user('nonexistant')
            
    @mock.patch('business.user.User', return_value=MockUser())
    def test_get_user_happy_case(self, mock_user):
        self.assertEquals(api.get_user('exists'), MOCK_USER_ENTRY)
        
    @mock.patch('business.user.User', return_value=MockUser())
    def test_get_all_users_happy_case(self, mock_user):
        self.assertEquals(api.get_all_users(), {
            MOCK_USER_ENTRY['UserID']: MOCK_USER_ENTRY
        })
        
    @mock.patch('business.user.User', return_value=MockUser())
    def test_add_user_id_already_exists(self, mock_user):
        with self.assertRaises(ValueError):
            api.add_user('exists', 'foo', 'bar')
    
    @mock.patch('business.user.User', return_value=MockUser())
    def test_add_user_invalid_id(self, mock_user):
        with self.assertRaises(ValueError):
            api.add_user('user', 'foo', 'bar')
        
    @mock.patch('business.user.User', return_value=MockUser())
    def test_add_user_invalid_name(self, mock_user):
        with self.assertRaises(ValueError):
            api.add_user('useruser', '', '')
        
    @mock.patch('business.user.User', return_value=MockUser())
    def test_add_user_happy_case(self, mock_user):
        api.add_user('useruser', 'foo', 'bar')
        
    @mock.patch('business.user.User', return_value=MockUser())
    def test_update_user_balance_nonexistant_user(self, mock_user):
        with self.assertRaises(ValueError):
            api.update_user_balance('nonexistant', 0)
            
    @mock.patch('business.user.User', return_value=MockUser())
    def test_update_user_balance_invalid_final_balance(self, mock_user):
        with self.assertRaises(ValueError):
            api.update_user_balance('exists', -1)
            
    @mock.patch('business.user.User', return_value=MockUser())
    def test_update_user_balance_happy_case(self, mock_user):
        api.update_user_balance('exists', 1)