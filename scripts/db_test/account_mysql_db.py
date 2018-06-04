import settings

from models.account_model import AccountModel
import hashlib

import random
import string
import json


def add_account_test():
    md5 = hashlib.md5()
    md5.update('123456')
    password = md5.hexdigest()
    insert_param = {
        "username": '2014024008' + str(random.randint(0,99)),
        "password": password,
        "level": 0
    }

    mm = AccountModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function add_account() return : %s " % mm.add_account(insert_param)

def get_account_by_user_id_test():
    user_id_to_get = 5

    mm = AccountModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function get_account_by_user_id() return : %s " % json.dumps(mm.get_account_by_user_id(user_id_to_get), indent=4)

def update_account_info_by_user_id_test():
    user_id_to_update = 6
    update_param = {
        "username": 'This is for update testing'
    }

    mm = AccountModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function update_account_info_by_user_id() return : %s " % mm.update_account_info_by_user_id(user_id_to_update, update_param)


def delete_account_by_user_id_test():
    user_id_to_delete = 7

    mm = AccountModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function delete_account_by_user_id() return : %s " % mm.delete_account_by_user_id(user_id_to_delete)


if __name__ == '__main__':
    
    # add_account_test()

    get_account_by_user_id_test()

    update_account_info_by_user_id_test()

    delete_account_by_user_id_test()