import json
import mock
import os
from unittest import TestCase


import boto3
import botocore
import moto


from business.database_table import DatabaseTable, DatabaseTableException


TABLE_STUB_PRIMARY_KEY = 'PrimaryKey'
MOCK_RESOURCE_NOT_FOUND_EXCEPTION = botocore.exceptions.ClientError({'Error': {'Code': 'ResourceNotFoundException'}}, 'op_name')
MOCK_CONDITIONAL_CHECK_EXCEPTION = botocore.exceptions.ClientError({'Error': {'Code': 'ConditionalCheckFailedException'}}, 'op_name')
MOCK_VALIDATION_EXCEPTION = botocore.exceptions.ClientError({'Error': {'Code': 'ValidationException'}}, 'op_name')
MOCK_TABLE_DESCRIPTION = {
    u'Table': {
        u'KeySchema': [
            {
                u'KeyType': u'HASH',
                u'AttributeName': TABLE_STUB_PRIMARY_KEY
            }
        ]
    }
}


class MockBoto3Client(object):
    def __init__(self, client_type, region_name='foo', table_exists=True):
        self.table_exists = table_exists
    
    def describe_table(self, TableName='foo'):
        if self.table_exists is False:
            raise MOCK_RESOURCE_NOT_FOUND_EXCEPTION
        else:
            return MOCK_TABLE_DESCRIPTION
            
class MockBoto3Resource(object):
    def __init__(self, client_type, region_name='foo'):
        pass
        
    def Table(self, table_name):
        return MockDynamoDBTable()

class MockDynamoDBTable(object):
    def __init__(self):
        self.table_data = json.loads(open(os.path.join(os.path.dirname(__file__), 'database_table_stub.json')).read())
    
    def scan(self):
        return {
            'Items': self.table_data
        }
        
    def get_item(self, Key=None):
        for row in self.table_data:
            if row[TABLE_STUB_PRIMARY_KEY] == Key[TABLE_STUB_PRIMARY_KEY]:
                return {
                    'Item': row
                }
        return {}
        
    def put_item(self, Item=None, ConditionExpression=''):
        try:
            if Item.has_key(TABLE_STUB_PRIMARY_KEY) is False:
                raise MOCK_VALIDATION_EXCEPTION
            
            for row in self.table_data:
                if row[TABLE_STUB_PRIMARY_KEY] == Item[TABLE_STUB_PRIMARY_KEY]:
                    raise MOCK_CONDITIONAL_CHECK_EXCEPTION
                    
            self.table_data.append(Item)
        except KeyError:
            raise MOCK_VALIDATION_EXCEPTION

    def delete_item(self, Key=None, ConditionExpression=''):         
        for row in self.table_data:
            if row[TABLE_STUB_PRIMARY_KEY] == Key[TABLE_STUB_PRIMARY_KEY]:
                self.table_data.remove(row)
                return
        raise MOCK_CONDITIONAL_CHECK_EXCEPTION
        
    def update_item(self, Key=None, ConditionExpression='', ExpressionAttributeValues='', UpdateExpression=''):
        if TABLE_STUB_PRIMARY_KEY in UpdateExpression:
            raise MOCK_VALIDATION_EXCEPTION
            
        for row in self.table_data:
            if row[TABLE_STUB_PRIMARY_KEY] == Key[TABLE_STUB_PRIMARY_KEY]:
                return
        raise MOCK_CONDITIONAL_CHECK_EXCEPTION


class TestUnitDatabaseTableInitialization(TestCase):
    @mock.patch('boto3.resource', return_value=mock.Mock())
    @mock.patch('boto3.client', return_value=MockBoto3Client('dynamodb', table_exists=False))
    def test_initalize_database_table_nonexistant_table(self, mock_boto3_resource, mock_boto3_client):
        with self.assertRaises(DatabaseTableException):
            DatabaseTable('nonexistant')
            
    @mock.patch('boto3.resource', return_value=mock.Mock())
    @mock.patch('boto3.client', return_value=MockBoto3Client('dynamodb', table_exists=True))
    def test_initalize_database_table_happy_case(self, mock_boto3_resource, mock_boto3_client):
        DatabaseTable('exists')
        
class TestUnitDatabaseTable(TestCase):
    @mock.patch('boto3.resource', return_value=MockBoto3Resource('dynamodb'))
    @mock.patch('boto3.client', return_value=MockBoto3Client('dynamodb', table_exists=True))
    def setUp(self, mock_boto3_resource, mock_boto3_client):
        self.test_table = DatabaseTable('foo')
        
    def test_get_row_nonexistant(self):
        with self.assertRaises(DatabaseTableException):
            self.test_table.get_row('gamma')
            
    def test_get_row_happy_case(self):
        self.assertEquals(self.test_table.get_row('alpha')['foo'], 'bar')
        
    def test_put_row_bad_primary_key(self):
        with self.assertRaises(DatabaseTableException):
            self.test_table.put_row(**{'bad': 'data'})
            
    def test_put_row_already_exists(self):
        with self.assertRaises(DatabaseTableException):
            self.test_table.put_row(**{TABLE_STUB_PRIMARY_KEY: 'alpha'})
            
    def test_put_row_happy_case(self):
        self.test_table.put_row(**{TABLE_STUB_PRIMARY_KEY: 'gamma', 'foo': 'foofoo'})
        
        self.assertEquals(self.test_table.get_row('gamma')['foo'], 'foofoo')
        
    def test_delete_row_nonexistant(self):
        with self.assertRaises(DatabaseTableException):
            self.test_table.delete_row('gamma')
            
    def test_delete_row_happy_case(self):
        self.test_table.delete_row('alpha')
        
        with self.assertRaises(DatabaseTableException):
            self.test_table.get_row('alpha')
            
    def test_update_row_nonexistant(self):
        with self.assertRaises(DatabaseTableException):
            self.test_table.update_row('gamma', **{'foo': 'bar'})
            
    def test_update_row_illegal_modification_of_primary_key(self):
        with self.assertRaises(DatabaseTableException):
            self.test_table.update_row('alpha', **{TABLE_STUB_PRIMARY_KEY: 'bar'})
            
    def test_update_row_happy_case(self):
        self.test_table.update_row('alpha', **{'foo': 'bar'})

    def test_get_all_rows(self):
        test_rows = self.test_table.get_all_rows()
        
        self.assertEquals(test_rows, self.test_table._table.table_data)