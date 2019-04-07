from business import database_table
from business import user


def get_user(user_id):
    try:
        table = user.User()

        return table.get_user(user_id)
    except database_table.DatabaseTableException as database_exception:
        raise ValueError(database_exception.message)

def get_all_users():
    table = user.User()

    return table.get_all_users()

def add_user(user_id, first_name, last_name):
    try:
        table = user.User()

        table.put_user(user_id, first_name, last_name)
    except (user.UserException, database_table.DatabaseTableException) as add_user_exception:
        raise ValueError(add_user_exception.message)
    
def update_user_balance(user_id, balance_update_amount):
    try:
        table = user.User()
        
        table.update_user_balance(user_id, balance_update_amount)
    except (user.UserException, database_table.DatabaseTableException) as add_user_exception:
        raise ValueError(add_user_exception.message)
