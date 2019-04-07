import decimal


import boto3
import botocore


SECRET_ACCESS_ID = 'AKIAJA4EKPXU5EPOJD2Q'
SECRET_ACCESS_KEY = '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'
BOTO_DECIMAL_PRECISION = 4

class DatabaseTableException(Exception):
    pass


class DatabaseTable(object):
    def __init__(self, table_name):
        self._dynamo_client = boto3.client('dynamodb', region_name='us-west-2', aws_access_key_id=SECRET_ACCESS_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
        self._dynamo_resource = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id=SECRET_ACCESS_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
        
        self._table_name = table_name
        
        self._check_if_table_exists()
        self._table = self._dynamo_resource.Table(table_name)
        
    def _check_if_table_exists(self):
        try:
            self._primary_key = self._dynamo_client.describe_table(TableName=self._table_name)['Table']['KeySchema'][0]['AttributeName']
        except botocore.exceptions.ClientError as client_error:
            if client_error.response['Error']['Code'] == 'ResourceNotFoundException':
                raise DatabaseTableException('Table "%s" does not exist.' % self._table_name)
            raise
        
    def get_row(self, index_value):
        try:
            response = self._table.get_item(
                Key={
                    self._primary_key: index_value
                }
            )
        
            return response['Item']
        except KeyError as key_error:
            raise DatabaseTableException('No row with primary key value of "%s" exists.' % index_value)
        
    def put_row(self, **kwargs):
        try:
            for key in kwargs:
                # Float types need to be stored as Decimals, otherwise we will get a runtime error.
                kwargs[key] = decimal.Decimal(str(round(kwargs[key], BOTO_DECIMAL_PRECISION))) if isinstance(kwargs[key], float) else kwargs[key]
            
            self._table.put_item(
                ConditionExpression='attribute_not_exists(%s)' % self._primary_key,
                Item=kwargs
            )
        except botocore.exceptions.ClientError as client_error:
            if client_error.response['Error']['Code'] == 'ValidationException':
                raise DatabaseTableException('Missing or invalid primary key "%s".' % self._primary_key)
            elif client_error.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise DatabaseTableException('Cannot put row: Row with primary key of value "%s" already exists.' % kwargs[self._primary_key])
            raise
            
    def delete_row(self, index_value):
        try:
            self._table.delete_item(
                ConditionExpression='attribute_exists(%s)' % self._primary_key,
                Key={
                    self._primary_key: index_value
                }
            )
        except botocore.exceptions.ClientError as client_error:
            if client_error.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise DatabaseTableException('Cannot delete row: No row with primary key "%s" exists in the table.' % index_value)
            raise

    def update_row(self, index_value, **kwargs):
        try:
            update_expressions = []
            expression_attribute_values = {}
            
            if not kwargs:
                raise DatabaseTableException('No update_row key value pairs provided.')
            elif self._primary_key in kwargs:
                raise DatabaseTableException('Cannot update row: Row modifications include changes to the primary key "%s".' % self._primary_key)
            
            for index, key in enumerate(kwargs):
                next_placeholder = 'val' + str(index)
                
                # Float types need to be stored as Decimals, otherwise we will get a runtime error.
                next_value = decimal.Decimal(str(round(kwargs[key], BOTO_DECIMAL_PRECISION))) if isinstance(kwargs[key], float) else kwargs[key]
                
                update_expressions.append('%s = :%s' % (key, next_placeholder))
                expression_attribute_values[':' + next_placeholder] = next_value
            
            self._table.update_item(
                ConditionExpression='attribute_exists(%s)' % self._primary_key,
                ExpressionAttributeValues=expression_attribute_values,
                Key={
                    self._primary_key: index_value
                },
                UpdateExpression='SET ' + ', '.join(update_expressions)
            )
        except botocore.exceptions.ClientError as client_error:
            if client_error.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise DatabaseTableException('Cannot update row: No row with primary key "%s" exists in the table.' % index_value)
            raise
    
    def get_all_rows(self):
        rows = self._table.scan()

        return rows['Items']

