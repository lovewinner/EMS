#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from utils.mysql.models.base_model import *


class AccountModel(BaseModel):

    _table_define = {
        'account': {
            'table_name': 'account',
            'table_fields': [
                ("`user_id`", "int(11)", "unsigned", "NOT NULL", "AUTO_INCREMENT"),
                ("`username`", "varchar(50)", "CHARACTER", "SET utf8", "NOT NULL", "DEFAULT", "''"),
                ("`password`", "char(50)", "CHARACTER", "SET utf8", "NOT NULL", "DEFAULT", "''"),
                ("`level`", "int(1)", "unsigned", "zerofill", "NOT NULL", "DEFAULT", "'0'"),
                ("`extra_info`", "text", "CHARACTER", "SET utf8"),
                ("`insert_time`", "int(11)", "NOT NULL", "DEFAULT", "'0'"),
                ("`update_time`", "int(11)", "NOT NULL", "DEFAULT", "'0'"),
            ]
        }
    }

    TABLE_NAME_ACCOUNT = 'account'

    ACCOUNT_LEVEL_NORMAL = 'normal'
    ACCOUNT_LEVEL_ADMIN = 'admin'
    ACCOUNT_LEVEL_SUPERADMIN = 'superadmin'

    ERROR_MESSAGE_NOT_USERNAME = '无效用户名！请重新输入并检查'
    ERROR_MESSAGE_NOT_PASSWORD = '密码错误！请重新输入'

    def __init__(self, db_list, db_conn_retry):
        BaseModel.__init__(self, db_list, db_conn_retry)

    def add_account(self, insert_param):
        return self._insert_table(table_name = self.TABLE_NAME_ACCOUNT, insert_param = insert_param)

    def get_account_by_user_id(self, user_id):
        select_param = {
            "user_id": user_id
        }
        return self._select_table(self.TABLE_NAME_ACCOUNT, select_param = select_param)

    def validate_account(self, validate_param):
        select_param = {
            "username": validate_param['username']
        }
        user_info = self._select_table(table_name = self.TABLE_NAME_ACCOUNT, select_param = select_param)
        if len(user_info) == 1:
            user_info = user_info[0]
            if validate_param['password'] == user_info['password']:
                return user_info
            else:
                return self.ERROR_MESSAGE_NOT_PASSWORD
        else:
            return self.ERROR_MESSAGE_NOT_USERNAME
        
    def update_account_info(self, user_id, update_param):
        keys = {
            "user_id": user_id
        }
        return self._update_table_by_key(table_name = self.TABLE_NAME_ACCOUNT, keys = keys, update_param = update_param)

    def delete_account_by_user_id(self, user_id):
        keys = {
            "user_id": user_id
        }
        return self._delete_table_by_key(table_name = self.TABLE_NAME_ACCOUNT, keys = keys)    
