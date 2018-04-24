#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import random
import copy
from pprint import pprint

class AbstractBalance :
    ##
    #  @machine_list : the machine list, it's a set.
    #   machine_list = [
    #      {"host":"127.0.0.1","port":3306,"mid":"pro1","is_master":False}, 
    #      {"host":"127.0.0.2","port":3306,"mid":"pro2","is_master":False}, 
    #      {"host":"127.0.0.3","port":3306,"mid":"pro3","is_master":True}
    #      ]
    ##
    def __init__(self, machine_list) :
        if self.__class__ is AbstractBalance :
            raise NotImplementedError, "Class %s does not implement __init__(self)" % self.__class__

        if False == isinstance(machine_list, list) :
            raise TypeError, "the type is invalied type(%s)" % type(machine_list).__name__

    def get_source(self, balance_param=None, balance_context=None) :
        if self.__class__ is AbstractBalance :
            raise NotImplementedError, "class %s does not implement get_source(self)" % self.__class__

    def mask_failed(self, mid) :
        if self.__class__ is AbstractBalance :
            raise NotImplementedError, "class %s does not implement mask_failed(self)" % self.__class__



class DBMasterSlaverRWBalance(AbstractBalance) :
    __machine_list = None
    __machine_list_dict = {}
    __machine_failed_time = None
    __has_machine_failed = None
    __master_id_index = None


    def __init__(self, machine_list) :
        AbstractBalance.__init__(self, machine_list)
        self.__machine_list = copy.deepcopy(machine_list)
        self.__machine_list_dict = {}
        #key:mid-val:failed_time
        self.__machine_failed_time = {}
        for m in machine_list :
            self.__machine_failed_time[m["mid"]] = 0
            self.__machine_list_dict[m["mid"]] = m
            if m["is_master"] :
                self.__master_id_index = machine_list.index(m)
        self.__has_machine_failed = False


    ##
    #   @balance_param : tell if need master
    #   balance_param = {"need_master":True}
    ##
    def get_source(self, balance_param, balance_context=None) :
        """
        Random to get the db, can make the Read/Write spliting
        Write : will always return the master db's machine_id
        Read : will return the machine_id from read+write randomly
        """
       
        if True == balance_param.get("need_master", False) :
            return self.__machine_list[self.__master_id_index] 
       
        # remove master, balance select slaver
        if len(self.__machine_list) > 1 and True == balance_param.get("need_slaver", False) :
            master_mid = self.__machine_list[self.__master_id_index]["mid"]
            del self.__machine_list_dict[master_mid]
            del self.__machine_list[self.__master_id_index]
         
        if False == self.__has_machine_failed :
            machine_num = len(self.__machine_list)
            randint = random.randint(0, machine_num-1)

            return self.__machine_list[randint] 
        else :
            #simply use roundrobin to select machine
            mink, minv = None, (1<<30)
            for (k,v) in self.__machine_failed_time.items() :
                if minv > v :
                    mink, minv = k, v
            return self.__machine_list_dict[mink]

        return None


    def mask_failed(self, machine_id) :
        """
        mask an failed machine
        """
        self.__machine_failed_time[machine_id] += 1
        self.__has_machine_failed = True
        return None


if __name__ == "__main__" :
    machine_list = [
       {"host":"127.0.0.1","port":3306,"mid":"pro1","is_master":False}, 
       {"host":"127.0.0.2","port":3306,"mid":"pro2","is_master":False}, 
       {"host":"127.0.0.3","port":3306,"mid":"pro3","is_master":True},
       {"host":"127.0.0.4","port":3306,"mid":"pro4","is_master":False}
       ]
    b = DBMasterSlaverRWBalance(machine_list)
    
    for i in range(0,7) :
        machine = b.get_source({"need_master":False})
        pprint(machine)
        b.mask_failed(machine["mid"]);

