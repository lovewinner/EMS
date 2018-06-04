import settings

from models.experiment_model import ExperimentModel
from models.account_model import AccountModel
import hashlib

import random
import string
import json
import time


def add_experiment_book_test():
    insert_param = {
        "experiment_id": random.randint(0,99),
        "user_id": random.randint(0,99),
        "experiment_place": ''.join(random.sample(string.ascii_letters + string.digits, 8)),
        "experiment_time": int(time.time())
    }

    mm = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function add_experiment_book() return : %s " % mm.add_experiment_book(insert_param)

def get_experiments_book_test():
    mm = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function get_experiments_book() return : %s " % json.dumps(mm.get_experiments_book(), indent=4)

def get_experiment_book_by_user_id_test():
    user_id_to_get = 2

    mm = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)
    print "\n>>>>>>>>> The result of the function get_experiment_book_by_user_id() return : %s " % json.dumps(mm.get_experiment_book_by_user_id(user_id_to_get), indent=4)

def update_experiment_book_by_book_id_test():
    book_id_to_update = 3
    update_param = {
        "experiment_place": "This is for update tesing"
    }

    mm = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)
    print "\n>>>>>>>>> The result of the function update_experiment_book_by_book_id() return : %s " % mm.update_experiment_book_by_book_id(book_id_to_update, update_param)

def delete_experiment_book_by_book_id_test():
    experiment_id_to_delete = 5

    mm = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)
    print "\n>>>>>>>>> The result of the function delete_experiment_book_by_book_id() return : %s " % mm.delete_experiment_book_by_book_id(experiment_id_to_delete)
    
if __name__ == '__main__':

    # add_experiment_book_test()

    get_experiments_book_test()

    get_experiment_book_by_user_id_test()

    update_experiment_book_by_book_id_test()

    # delete_experiment_book_by_book_id_test()
    


