import decimal


import database_table


USER_LIST_TABLE_NAME = 'UserList'
DEFAULT_USER_BALANCE = 30000


class UserException(Exception):
    pass


def _check_user_id(user_id):
    if len(user_id) < 6 or len(user_id) > 15:
        raise UserException('Invalid user id %s' % user_id)


def _check_balance(balance):
    if balance < 0:
        raise UserException('Invalid balance amount %d' % balance)


def _check_name(name):
    if len(name) == 0:
        raise UserException('Invalid user name %s' % name)


def _check_email_address(email_address):
    if '@' not in email_address:
        raise UserException('Invalid email address %s' % email_address)


class User(object):
    def __init__(self):
        self._user_table = database_table.DatabaseTable(USER_LIST_TABLE_NAME)

    def get_user(self, user_id):
        return self._user_table.get_row(user_id)

    def get_all_users(self):
        return self._user_table.get_all_rows()

    def put_user(self, user_id, first_name, last_name):
        _check_user_id(user_id)
        _check_name(first_name)
        _check_name(last_name)

        self._user_table.put_row(
            UserID=user_id,
            FirstName=first_name,
            LastName=last_name,
            Balance=DEFAULT_USER_BALANCE
        )
    
    def update_user_balance(self, user_id, balance_update_amount):
        user = self.get_user(user_id)
        new_balance = user['Balance'] + decimal.Decimal(balance_update_amount)
        
        _check_balance(new_balance)
        
        self._user_table.update_row(user_id, Balance=new_balance)
