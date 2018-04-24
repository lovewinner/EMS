#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
from pprint import pprint
from collections import OrderedDict

class AbstractSharding :
    def __init__(self) :
        if self.__class__ is AbstractSharding :
            raise NotImplementedError, "Class %s does not implement __init__(self)" % self.__class__

    def splitting_table(self, splitting_param) :
        if self.__class__ is AbstractSharding :
            raise NotImplementedError, "class %s does not implement splitting_param(self)" % self.__class__


class SegmentSharding(AbstractSharding) :
    def __init__(self) :
        AbstractSharding.__init__(self)
    ##
    #   * input param :
    #   @splitting_param : a dict, which is the segment information, like (seg_key, seg_per_table)
    #       splitting_param = {"seg_table":"user_contact", "seg_key":"seq_id", "seg_value":198349, "seg_per_table":1000}
    #   
    #   * return :
    #      a dict, which is the table name 
    #      return = {"table_name" : "users_100000"} 
    ##
    def splitting_table(self, splitting_param) :
        table_value = splitting_param["seg_value"] // splitting_param["seg_per_table"]
        return {"table_name" : "%s_%d" % (splitting_param["seg_table"], table_value)}

class DateSharding(AbstractSharding):
    def __init__(self):
        AbstractSharding.__init__(self)

    def splitting_table(self, splitting_param) :
        table_name = splitting_param['d_table'] + '_'
        timestamp = splitting_param['d_value']
        dt = datetime.datetime.fromtimestamp(timestamp)
        date = dt.strftime("%Y_%m_%d")
        return {"table_name" : table_name + date }

class MonthSharding(AbstractSharding):
    def __init__(self):
        AbstractSharding.__init__(self)

    def splitting_table(self, splitting_param) :
        table_name = splitting_param['d_table'] + '_'
        timestamp = splitting_param['d_value']
        dt = datetime.datetime.fromtimestamp(timestamp)
        date = dt.strftime("%Y_%m")
        return {"table_name" : table_name + date }

class TimeVersionSharding(AbstractSharding) :
    def __init__(self) :
        AbstractSharding.__init__(self)

    def splitting_table(self, splitting_param) :
        table_name = splitting_param['tv_table'] + '_'

        if "tv_time_mode" in splitting_param :
            time_mode = splitting_param['tv_time_mode']
            return {"table_name" : table_name + time_mode + '_' + str(splitting_param['tv_table_meta'][time_mode]['count'])}
        else :
            # select the min time
            tv_time_interval = sorted(splitting_param['tv_time_interval'].items(), key=lambda x:x[1])
            for (k, v) in tv_time_interval :
                tmp = splitting_param['tv_table_meta'][k]
                if splitting_param['tv_value'] >= tmp['start_time'] :
                    table_name += k + '_' + str(tmp['count'])
                    break
            return {"table_name" : table_name}
        return {"table_name" : ''}

class ConsistentHashSharding(AbstractSharding) :
    ##
    #   * input param :
    #   @splitting_param : a dict, which is the sharding information
    #       splitting_param = {"ch_table":"email_index", "ch_key":"email", "ch_value":"yuanhao@easilydo.com", "ch_table_num":2000}
    #
    #   * return :
    #      a dict, which is the table name 
    #      return = {"table_name" : "users_10000"} 
    ##
    def __init__(self) :
        AbstractSharding.__init__(self)

    def splitting_table(self, splitting_param) :
        table_value = hash(splitting_param["ch_value"]) % int(splitting_param["ch_table_num"])
        return {"table_name" : "%s_%d" % (splitting_param["ch_table"], table_value)}


if __name__ == "__main__" :
    #s = SegmentSharding()
    #splitting_param = {"seg_table":"user_contact", "seg_key":"seq_id", "seg_value":198349, "seg_per_table":1000}
    #res = s.splitting_table(splitting_param)
    #pprint(res)

    #splitting_param = {
    #    "tv_table":"report_interative_task", 
    #    "tv_key":"task_update_time", 
    #    "tv_value":1383899164,
    #    "tv_time_interval":{'1w':604800,'2w':1209600,'1m':2678400}, 
    #    "tv_table_meta":{
    #        "1w": {
    #            "start_time" : 1383899165,
    #            "count" : 2,
    #        },
    #        "2w": {
    #            "start_time" : 1383899162,
    #            "count" : 2,
    #        },
    #        "1m": {
    #            "start_time" : 1383899161,
    #            "count" : 1,
    #        }
    #    }
    #}
    #s = TimeVersionSharding()
    #res = s.splitting_table(splitting_param)
    #print res
    import time
    splitting_param = {
            "d_table": "monitor",
            "d_value": int(time.time()),
    }
    s = DateSharding()
    res = s.splitting_table(splitting_param)
    print res

    #s = ConsistentHashSharding()
    #splitting_param = {"ch_table":"email_index", "ch_key":"email", "ch_value":"wuyuanhao@easilydo.com", "ch_table_num":2000}
    #res = s.splitting_table(splitting_param)
 
