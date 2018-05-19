#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from utils.mysql.models.base_model import *

class ExperimentModel(BaseModel) :

    _table_define = {
        'experiment' : {
            'table_name': 'experiment',
            'table_fields': [
                ("`experiment_id`", "int(11)", "unsigned", "NOT", "NULL", "AUTO_INCREMENT"),
                ("`experiment_name`", "varchar(255)", "CHARACTER", "SET", "utf8", "NOT NULL", "DEFAULT", "''"),
                ("`experiment_content`", "text", "CHARACTER", "SET", "utf8"),
                ("`experiment_media`", "text", "CHARACTER", "SET", "utf8"),
                ("`extra_info`", "text", "CHARACTER", "SET", "utf8"),
                ("`insert_time`", "int(11)", "NOT", "NULL"),
                ("`update_time`", "int(11)", "NOT", "NULL"),
            ]
        },

        'experiment_book': {
            'table_name': 'experiment_book',
            'table_fields': [
                ("`book_id`", "int(11)", "unsigned", "NOT", "NULL", "AUTO_INCREMENT"),
                ("`experiment_id`", "int(11)", "unsigned", "NOT", "NULL"),
                ("`user_id`", "int(11)", "unsigned", "NOT", "NULL"),
                ("`experiment_place`", "text", "CHARACTER", "SET", "utf8", "NOT", "NULL"),
                ("`experiment_time`", "int(11)", "NOT NULL", "DEFAULT"," '0'"),
                ("`extra_info`", "text", "CHARACTER", "SET", "utf8"),
                ("`insert_time`", "int(11)", "NOT", "NULL"),
                ("`update_time`", "int(11)", "NOT", "NULL"),
            ]
        },

        'experiment_publish': {
            'table_name': 'experiment_publish',
            'table_fields': [
                ("`publish_id`", "int(11)", "unsigned", "NOT NULL", "AUTO_INCREMENT"),
                ("`experiment_id`", "int(11)", "NOT NULL"),
                ("`experiment_place`", "text", "CHARACTER", "SET utf8", "NOT NULL"),
                ("`experiment_time`", "text", "CHARACTER", "SET utf8", "NOT NULL"),
                ("`publish_belong`", "int(11)", "NOTNULL"),
                ("`extra_info`", "text", "CHARACTER", "SET utf8"),
                ("`insert_time`", "int(11)", "NOT NULL"),
                ("`update_time`", "int(11)", "NOT NULL"),
            ]
        }
    }

    TABLE_NAME_EXPERIMENT = 'experiment'
    TABLE_NAME_EXPERIMENT_BOOK = 'experiment_book'
    TABLE_NAME_EXPERIMENT_PUBLISH = 'experiment_publish'

    def __init__(self, db_list, db_conn_retry):
        BaseModel.__init__(self, db_list, db_conn_retry)


    # Experiment
    def add_experiment(self, insert_param):
        return self._insert_table(table_name = self.TABLE_NAME_EXPERIMENT, insert_param = insert_param)

    def get_experiments(self):
        return self._select_table(table_name = self.TABLE_NAME_EXPERIMENT, select_param = '1')

    def get_experiments_by_name(self, experiment_name):
        select_param = {
            "experiment_name": experiment_name
        }
        return self._select_table(table_name=self.TABLE_NAME_EXPERIMENT, select_param=select_param)    

    def update_experiment_by_experiment_id(self, experiment_id, update_param):
        keys = {
            "experiment_id": experiment_id
        }
        return self._update_table_by_key(table_name = self.TABLE_NAME_EXPERIMENT, keys = keys, update_param = update_param)

    def delete_experiment_by_experiment_id(self, experiment_id):
        keys = {
            "experiment_id": experiment_id
        }
        return self._delete_table_by_key(table_name = self.TABLE_NAME_EXPERIMENT, keys = keys)

    # Experiment Book
    def add_experiment_book(self, insert_param):
        return self._insert_table(table_name = self.TABLE_NAME_EXPERIMENT_BOOK, insert_param = insert_param)

    def get_experiment_book_by_user_id(self, user_id):
        select_param = {
            "user_id": user_id
        }
        return self._select_table(table_name = self.TABLE_NAME_EXPERIMENT_BOOK, select_param = select_param)

    def update_experiment_book_by_book_id(self, book_id, update_param):
        keys = {
            "book_id": book_id
        }
        return self._update_table_by_key(table_name = self.TABLE_NAME_EXPERIMENT_BOOK, keys = keys, update_param = update_param)
    
    def delete_experiment_book_by_book_id(self, book_id):
        keys = {
            "book_id": book_id
        }
        return self._delete_table_by_key(table_name=self.TABLE_NAME_EXPERIMENT, keys=keys)

    # Experiment Publish
    def add_experiment_publish(self, insert_param):
        return self._insert_table(table_name=self.TABLE_NAME_EXPERIMENT_PUBLISH, insert_param=insert_param)

    def get_experiment_publish_by_experiment_id(self, experiment_id):
        select_param = {
            "experiment_id": experiment_id
        }
        return self._select_table(table_name=self.TABLE_NAME_EXPERIMENT_PUBLISH, select_param=select_param)

    def update_experiment_publish_by_publish_id(self, publish_id, update_param):
        keys = {
            "publish_id": publish_id
        }
        return self._update_table_by_key(table_name=self.TABLE_NAME_EXPERIMENT_PUBLISH, keys=keys, update_param=update_param)

    def delete_experiment_publish_by_publish_id(self, publish_id):
        keys = {
            "publish_id": publish_id
        }
        return self._delete_table_by_key(table_name=self.TABLE_NAME_EXPERIMENT_PUBLISH, keys=keys)