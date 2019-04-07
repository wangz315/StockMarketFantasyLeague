from decimal import Decimal
import json
import mock
import os
from unittest import TestCase


from business.database_table import DatabaseTableException
import business.user


PRIMARY_KEY = 'UserID'


class MockDatabaseTable(object):
    def __init__(self):
        self.table_data = json.loads(open(os.path.join(os.path.dirname(__file__), 'userlist_stub.json')).read())
        
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
                result['Balance'] = Decimal(result['Balance'])
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


class TestUnitUser(TestCase):
    @mock.patch('business.database_table.DatabaseTable', return_value=MockDatabaseTable())
    def setUp(self, mock_database_table):
        self.test_user = business.user.User()

    def test_get_user_nonexistant_user(self):
        with self.assertRaises(DatabaseTableException):
            self.test_user.get_user('nonexistant')

    def test_get_user_happy_case(self):
        self.assertEquals(self.test_user.get_user('alpha1992')['FirstName'], 'alpha')

    def test_put_user_happy_case(self):
        self.test_user.put_user('tomy2005', 'tom', 'hardy')
        
        self.assertEquals(self.test_user.get_user('tomy2005')['FirstName'], 'tom')

    def test_put_user_duplicate(self):
        with self.assertRaises(DatabaseTableException):
            self.test_user.put_user('alpha1992', 'tom', 'hardy')
            
    def test_get_all_users_happy_case(self):
        self.assertEquals(self.test_user.get_all_users(), self.test_user._user_table.table_data)

    def test_update_user_balance_nonexistant_user(self):
        with self.assertRaises(DatabaseTableException):
            self.test_user.update_user_balance('nonexistant', 0)

    def test_update_user_balance_invalid_final_balance(self):
        with self.assertRaises(business.user.UserException):
            self.test_user.update_user_balance('alpha1992', '-40000')
        
        
    def test_update_user_balance_happy_case(self):
        self.test_user.update_user_balance('alpha1992', 1)


class TestUnitUserValidators(TestCase):
    def test_check_name_empty_string(self):
        with self.assertRaises(business.user.UserException):
            business.user._check_name('')

    def test_check_name_happy_case(self):
        business.user._check_name('panther')

    def test_check_user_id_string_too_short(self):
        with self.assertRaises(business.user.UserException):
            business.user._check_user_id('tom07')

    def test_check_user_id_string_too_long(self):
        with self.assertRaises(business.user.UserException):
            business.user._check_user_id('bellagioHotel2007')

    def test_check_user_id_happy_case(self):
        business.user._check_user_id('hardy1989')

    def test_check_balance_negative_balance(self):
        with self.assertRaises(business.user.UserException):
            business.user._check_balance(-22)

    def test_check_balance_happy_case(self):
        business.user._check_balance(3000)

    def test_check_email_address_invalid_id(self):
        with self.assertRaises(business.user.UserException):
            business.user._check_email_address('tomhardyAtTheRategmail.com')

    def test_check_email_address_happy_case(self):
        business.user._check_email_address('tomhardy.89@gmail.com')