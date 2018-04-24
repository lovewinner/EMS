#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from mysql_dal.models.base_model import *

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
