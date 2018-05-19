import settings

from models.experiment_model import ExperimentModel
from models.account_model import AccountModel
import hashlib

if __name__ == '__main__':
    mm = ExperimentModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)
    user = AccountModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)
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

    user_info = {
        "username": '201402400803',
        "password": hashlib.md5('123456').hexdigest(),
        "extra_info": '{query: 123}'
    }

    print user.update_account_info(2, user_info)
