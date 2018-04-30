import settings

from models.experiment_model import ExperimentModel

if __name__ == '__main__':
    mm = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    insert_param = {
        "experiment_name": 'insert_test',
        "experiment_content": '11111',
        "experiment_media": '22222',
        "extra_info": '0',
        "insert_time": '1',
        "update_time": '2',
    }

    update_param = {
        "experiment_name": 'update_test'
    }
    print mm.delete_experiment_by_id('2')
