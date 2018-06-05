import settings

from models.experiment_model import ExperimentModel
from models.account_model import AccountModel
import hashlib

import random
import string
import json
import time


def add_experiment_publish_test():
    insert_param = {
        "experiment_id": random.randint(0,99),
        "publish_belong": random.randint(0,99),
        "experiment_place": ''.join(random.sample(string.ascii_letters + string.digits, 8)),
        "experiment_time": int(time.time())
    }

    experiment = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function add_experiment_publish() return : %s " % experiment.add_experiment_publish(insert_param)

def get_experiments_publish_test():
    experiment = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function get_experiments_publish() return : %s " % json.dumps(experiment.get_experiments_publish(), indent=4)

def get_experiment_publish_by_experiment_id_test():
    experiment_id_to_get = 73

    experiment = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)
    print "\n>>>>>>>>> The result of the function get_experiment_publish_by_experiment_id() return : %s " % json.dumps(experiment.get_experiment_publish_by_experiment_id(experiment_id_to_get), indent=4)

def update_experiment_publish_by_publish_id_test():
    book_id_to_update = 3
    update_param = {
        "experiment_place": "This is for update tesing"
    }

    experiment = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)
    print "\n>>>>>>>>> The result of the function update_experiment_publish_by_publish_id() return : %s " % experiment.update_experiment_publish_by_publish_id(book_id_to_update, update_param)

def delete_experiment_publish_by_publish_id_test():
    experiment_id_to_delete = 5

    experiment = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)
    print "\n>>>>>>>>> The result of the function delete_experiment_publish_by_publish_id() return : %s " % experiment.delete_experiment_publish_by_publish_id(experiment_id_to_delete)
    
if __name__ == '__main__':

    # add_experiment_publish_test()

    get_experiments_publish_test()

    get_experiment_publish_by_experiment_id_test()

    update_experiment_publish_by_publish_id_test()

    # delete_experiment_publish_by_publish_id_test()
    


