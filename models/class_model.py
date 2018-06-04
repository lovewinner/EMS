#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from utils.mysql.models.base_model import *


class ClassModel(BaseModel):

    _table_define = {
        'classes': {
            'table_name': 'classes',
            'table_fields': [
                ("`id`", "int(11)", "unsigned", "NOT NULL", "AUTO_INCREMENT"),
                ("`name`", "varchar(255)", "CHARACTER", "SET utf8", "NOT NULL", "DEFAULT ''"),
                ("`insert_time`", "int(11)", "NOT", "NULL"),
                ("`update_time`", "int(11)", "NOT", "NULL"),
            ]
        }
    }

    TABLE_NAME = 'classes'

    def __init__(self, db_list, db_conn_retry):
        BaseModel.__init__(self, db_list, db_conn_retry)

    def add_class(self, insert_param):
        return self._insert_table(table_name = self.TABLE_NAME, insert_param = insert_param)

    def get_classes(self):
        return self._select_table(table_name = self.TABLE_NAME, select_param = '1')

    def update_class_by_class_id(self, class_id, update_param):
        keys = {
            "id": class_id
        }
        return self._update_table_by_key(table_name = self.TABLE_NAME, keys = keys, update_param = update_param)

    def delete_class_by_class_id(self, class_id):
        keys = {
            "id": class_id
        }
        return self._delete_table_by_key(table_name = self.TABLE_NAME, keys = keys)