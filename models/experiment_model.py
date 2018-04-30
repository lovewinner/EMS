#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import sys
sys.path.append("..")

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

    def __init__(self, db_list, db_conn_retry):
        BaseModel.__init__(self, db_list, db_conn_retry)


    # Experiment
    def add_experiment(self, insert_param):
        return self._insert_table(table_name = 'experiment', insert_param = insert_param)

    def get_experiments(self):
        return self._select_table(table_name = 'experiment', select_param = '1')

    def get_experiments_by_name(self, experiment_name):
        select_param = {
            "experiment_name": experiment_name
        }
        return self._select_table(table_name='experiment', select_param=select_param)    

    def update_experiment_by_id(self, experiment_id, update_param):
        keys = {
            "experiment_id": experiment_id
        }
        return self._update_table_by_key(table_name = 'experiment', keys = keys, update_param = update_param)

    def delete_experiment_by_id(self, experiment_id):
        keys = {
            "experiment_id": experiment_id
        }
        return self._delete_table_by_key(table_name = 'experiment', keys = keys)
