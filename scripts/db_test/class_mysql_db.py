import settings

from models.class_model import ClassModel

import random
import string
import json

def add_class_test():
    insert_param = {
        "name": ''.join(random.sample(string.ascii_letters + string.digits, 8))
    }

    mm = ClassModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function add_class() return : %s " % mm.add_class(insert_param)

def get_classes_test():
    mm = ClassModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function get_classes() return : %s " % json.dumps(mm.get_classes(), indent=4)

def update_class_by_class_id_test():
    class_id_to_update = 4
    update_param = {
        "name": 'This is for update testing'
    }

    mm = ClassModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function update_class_by_class_id() return : %s " % mm.update_class_by_class_id(class_id_to_update, update_param)

def delete_class_by_class_id_test():
    class_id_to_delete = 6

    mm = ClassModel(settings.DB_CONFIGURE, settings.DB_CONN_RETRY)

    print "\n>>>>>>>>> The result of the function delete_class_by_class_id() return : %s " % mm.delete_class_by_class_id(class_id_to_delete)

if __name__ == '__main__':
    
    # add_class_test()

    get_classes_test()

    update_class_by_class_id_test()

    # delete_class_by_class_id_test()
