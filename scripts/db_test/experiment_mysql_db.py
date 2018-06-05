import settings

from models.experiment_model import ExperimentModel

import random
import string
import json


def add_experiment_test():
    insert_param = {
        "experiment_name": ''.join(random.sample(string.ascii_letters + string.digits, 8)),
        "experiment_content": ''.join(random.sample(string.ascii_letters + string.digits, 8)),
        "experiment_media": ''.join(random.sample(string.ascii_letters + string.digits, 8))
    }

    experiment = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function add_experiment() return : %s " % experiment.add_experiment(insert_param)

def get_experiments_test():
    experiment = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function get_experiments() return : %s " % json.dumps(experiment.get_experiments(), indent=4)

def get_experiments_by_name_test():
    experiment = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function get_experiments_by_name() return : %s " % json.dumps(experiment.get_experiments_by_name('select_by_name_test'), indent=4)    

def get_experiment_by_experiment_id_test():
    experiment = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function get_experiment_by_experiment_id() return : %s " % json.dumps(experiment.get_experiment_by_experiment_id(1), indent=4)

def update_experiment_by_experiment_id_test():
    update_param = {
        "experiment_content": "This is for update tesing"
    }

    experiment = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)
    print "\n>>>>>>>>> The result of the function update_experiment_by_id() return : %s " % experiment.update_experiment_by_experiment_id(3, update_param)

def delete_experiment_by_experiment_id_test():
    experiment_id_to_delete = 14
    experiment = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function delete_experiment_by_experiment_id() return : %s " % experiment.delete_experiment_by_experiment_id(experiment_id_to_delete)
    
if __name__ == '__main__':

    # add_experiment_test()

    get_experiments_test()

    get_experiments_by_name_test()

    get_experiment_by_experiment_id_test()

    update_experiment_by_experiment_id_test()

    # delete_experiment_by_experiment_id_test()
    


