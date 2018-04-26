#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import _mysql_exceptions
import sys,os
from pprint import pprint
import new
import copy
import json
import time
import datetime
from weakref import proxy
from mysql.libraries.balance import *
from mysql.libraries import sharding
import logging
import socket

logger = logging.getLogger('mysql_query')


class MyCursor(object):
    def __init__(self, base_model, cursor_cls=MySQLdb.cursors.DictCursor):
        self._base_model = proxy(base_model)
        self._cursor_cls = cursor_cls
        self._cursor = None

    def __getattr__(self, name):
        return getattr(self._cursor, name)

    def connect(self):
        self._cursor = self._base_model._db_conn.cursor(self._cursor_cls)

    def close(self):
        if self._cursor != None:
            self._cursor.close()
        self._cursor = None

    def _execute(self, *args, **kwargs):
        for i in range(2):
            try:
                if self._cursor is None:
                    self._base_model._get_db()
                    self.connect()
                return self._cursor.execute(*args, **kwargs)
            except _mysql_exceptions.OperationalError as e:
                #2014 for https://easilydo.atlassian.net/browse/SIFT-595
                logging.warning("run fail[e: %s, args: %s, kwargs: %s]", e, args, kwargs)
                if e[0] in [2013, 2006, 2014]:
                    self._base_model.db_free()
                    self._base_model._get_db()
                    continue
                else:
                    raise
            except Exception as e:
                raise
        return None

    def execute(self, *args, **kwargs):
        begin_time = time.time() * 1000
        res = self._execute(*args, **kwargs)
        runtime = int(time.time() * 1000 - begin_time)
        logger.info("execute sql[runtime: %d, args: %s, kwargs: %s]", runtime, args, kwargs)
        return res


class BaseModel(object):
    """
    The base model for all models which define some base method and variable
    """
    __GEN_LINE_BREAK = "\n"
    _table_define= {}

    _db_conn = None
    _db_is_master = False

    _db_list = []
    _db_conn_retry = 0
    _timeout = 10
    _charset = 'utf8'


    def __init__(self, db_list, db_conn_retry=3) :
        for (k, v) in self._table_define.items() :
            tmp = []
            for vv in v['table_fields'] :
                tmp.append(vv[0])
            self._table_define[k]['table_fields_key'] = tmp[:]

        self._db_list = db_list
        self._db_conn_retry = db_conn_retry
        self._db_cursor = MyCursor(self)

    def __del__(self) :
        self.__db_free()

    def db_free(self) :
        self.__db_free()

    def __db_free(self) :
        self._db_cursor.close()
        if None != self._db_conn :
            self._db_conn.close()
            self._db_conn = None

    def __get_db_conn(self, need_master) :
        """
        get an database connection
        """
        # build mid
        i = 0
        for v in self._db_list :
            v['mid'] = str(i) + '_' + v['host'] + '_' + str(v['port'])
            i+=1
        # balance connected
        self.__db_free()
        bal = DBMasterSlaverRWBalance(self._db_list)

        db_conn = None
        db = None
        flag = False
        retry = self._db_conn_retry
        while retry>0 :
            try :
                db = bal.get_source({"need_master":need_master})
                logging.debug("balance get_resource get_db. host[%s] mid[%s]", db['host'], db['mid'])
                host = socket.gethostbyname(db['host'])
                db_conn = MySQLdb.connect(host=host, user=db['username'], passwd=db['password'],db=db['dbname'],charset=db['charset'],port=db['port'], connect_timeout=self._timeout)
                flag = True
                self._charset = db['charset']
            except Exception, e:
                logging.warning("connect to mysql failed. host[%s] mid[%s]. retry_remain[%d] e[%s]" % (db['host'], db['mid'], retry, e), exc_info=True)
                bal.mask_failed(db["mid"])
            retry -= 1
            if flag :
                break
            time.sleep(3)

        if False == flag :
            logging.warning("Can not connect to mysql")
            return None, None
        return db_conn, db


    def _get_db(self) :
        if None != self._db_conn :
            return self._db_conn

        self.__db_free()
        #init the database
        (self._db_conn, db) = self.__get_db_conn(need_master=False)
        if (None == self._db_conn) :
            raise RuntimeError, "RuntimeError get db connection failed class[%s] __init__(self)" % self.__class__
        self._db_cursor.connect()
        if 'utf8mb4' == self._charset :
            self._db_cursor.execute("set names utf8mb4 collate utf8mb4_unicode_ci;")
        self._db_cursor.execute("set autocommit=1;")

        self._db_is_master = db['is_master']
        return self._db_conn


    def _change_to_master(self) :
        """
        change the db connection to the master
        """
        if False == self._db_is_master :
            (self._db_conn, db) = self.__get_db_conn(need_master=True)
            self._db_is_master = True
            self._db_cursor.connect()
            self._db_cursor.execute("set autocommit=1;")
        return self._get_db()


    def _get_sharding_table_name(self, table_name, sharding_data) :
        """
        get the sharding table name
        """
        amod = sharding
        aclass= getattr(amod, self._table_define[table_name]['sharding_method'])
        s = aclass()
        splitting_param = {}
        if 'SegmentSharding' ==  self._table_define[table_name]['sharding_method'] :
            splitting_param = {
                "seg_table" : table_name,
                "seg_key" : self._table_define[table_name]['sharding_seg_key'],
                "seg_value" : sharding_data[self._table_define[table_name]['sharding_seg_key']],
                "seg_per_table": self._table_define[table_name]['sharding_seg_per_table'],
                }
        elif self._table_define[table_name]['sharding_method'] in ['DateSharding', 'MonthSharding']:
            d_value = sharding_data.get("timestamp")
            if not d_value:
                d_value = int(time.time())
            splitting_param = {
                "d_table": table_name,
                "d_value": d_value,
                }
        elif 'TimeVersionSharding' == self._table_define[table_name]['sharding_method']:
            splitting_param = {
                "tv_table" : table_name,
                "tv_key" : self._table_define[table_name]['sharding_tv_key'],
                "tv_value" : sharding_data[self._table_define[table_name]['sharding_tv_key']],
                "tv_time_interval" : self._table_define[table_name]['sharding_time_interval'],
                "tv_time_mode" : sharding_data["time_mode"],
            }
            # get table meta from db
            sql = "SELECT `table_name`, `meta_object` FROM `%s_table_meta`" % (table_name)
            row = {}
            try :
                res = self._db_cursor.execute(sql)
                row = self._db_cursor.fetchallDict()
            except Exception, e :
                logging.warning('select mysql failed! exception[%s] sql[%s]' % (e, sql))
                return False
            splitting_param['tv_table_meta'] = json.loads(row[0]['meta_object'])
        elif 'ConsistentHashSharding' == self._table_define[table_name]['sharding_method'] :
            splitting_param = {
                "ch_table" : table_name,
                "ch_key" : self._table_define[table_name]['sharding_ch_key'],
                "ch_value" : sharding_data[self._table_define[table_name]['sharding_ch_key']],
                "ch_table_num" : self._table_define[table_name]['sharding_ch_table_num'],
            }
        return s.splitting_table(splitting_param)


    def _gen_insert_sql(self, insert_param, need_escape=True) :
        """
        from a dict param to insert sql
        """
        # insert_param = {
        #       'table_name' : 'user_contact'
        #       'field_values' : {
        #           'user_id' : 13123,
        #           'contact_id' : "124-abcd-efg",
        #           'colmmn_name' : "col_v"
        #       }
        #    }
        sql = 'INSERT INTO `%s`(' % insert_param['table_name']
        sql_keys = '';
        for v in insert_param['field_values'].keys() :
            sql_keys += "`%s`," % v
        sql_keys = sql_keys.rstrip(',')
        sql += sql_keys + ") VALUES(";
        sql_values = '';
        for v in insert_param['field_values'].values() :
            sql_values += "%s," % self.__escape_string(v, need_escape)
        sql_values = sql_values.rstrip(',')
        sql += sql_values + ")"
        return sql


    def _gen_update_sql(self, update_param, need_escape=True) :
        """
        from a dict param to update sql
        """
        # insert_param = {
        #       'table_name' : 'user_contact'
        #       'field_values' : {
        #           'user_id' : 13123,
        #           'contact_id' : "124-abcd-efg",
        #           'colmmn_name' : "col_v"
        #       }
        #       'where' : 'user_id=100'
        #    }
        sql = 'UPDATE `%s` SET' %  update_param['table_name']
        sql_set = ''
        for (k, v) in update_param['field_values'].items() :
            sql_set += " `%s`=%s," % (k, self.__escape_string(v, need_escape))
        sql_set = sql_set.rstrip(',')
        sql += sql_set
        if 'str' == type(update_param['where']).__name__ or 'unicode' == type(update_param['where']).__name__:
            sql += " WHERE %s" % update_param['where']
        elif isinstance(update_param['where'], dict) :
            sql += self.__gen_where(update_param['where'])
        else :
            sql = ''
        return sql


    def _gen_delete_sql(self, delete_param) :
        """
        from a dict param to delete sql
        """
        sql = "DELETE FROM `%s`" % delete_param['table_name']
        if 'str' == type(delete_param['where']).__name__ or 'unicode' == type(delete_param['where']).__name__:
            sql += " WHERE %s" % delete_param['where']
        elif isinstance(delete_param['where'], dict) :
            sql += self.__gen_where(delete_param['where'])
        else :
            sql = ''
        return sql


    def _gen_select_sql(self, select_param) :
        """
        from a dict param to select sql
        """
        sql = "SELECT "
        sql_fields = ''
        for v in select_param['fields'] :
            sql_fields += '%s,' % v
        sql += sql_fields.rstrip(',')
        sql += " FROM `%s`" % select_param['table_name']
        force_index = select_param.get('force_index', '')
        if '' != force_index :
            sql += ' FORCE INDEX(`%s`)' % force_index
        if 'str' == type(select_param['where']).__name__ or 'unicode' == type(select_param['where']).__name__:
            sql += " WHERE %s" % select_param['where']
        #if 'dict' == type(select_param['where']).__name__ :
        if isinstance(select_param['where'], dict) and {} != select_param['where']:
            sql += self.__gen_where(select_param['where'])
        if select_param.get('order_by') :
            order_by = select_param.get('order_by')
            sql += " ORDER BY %s" % order_by
        if select_param.get('limit'):
            (offset, count) = select_param.get('limit')
            sql += " limit %d, %d" % (offset, count)
        return sql


    def __gen_where(self, where_dict) :
        tmp = " WHERE"
        flag = False
        for (k,v) in where_dict.items() :
            if flag :
                tmp += " AND `%s`=" % (k)
            else :
                tmp += " `%s`=" % (k)
                flag = True
            tmp += self.__escape_string(str(v))
        return tmp


    def __escape_string(self, v, need_escape=True) :
        """
        For the variable's type, escape it
        """
        if 'str' == type(v).__name__ or 'unicode' == type(v).__name__ :
            if need_escape :
                return "'%s'" % self._db_conn.escape_string(v.encode("utf8"))
            else :
                return "'%s'" % v
        elif 'int' == type(v).__name__  or 'long' == type(v).__name__ or 'float' == type(v).__name__ :
            return "%s" % v
        elif 'list' == type(v).__name__ :
            return "%s" % v[0]
        else :
            return None


    @classmethod
    def gen_create_table_sql(self, table_define) :
        """
        tool method can gen the create table from table_define.
        """
        #sql demo
        #DROP TABLE IF EXISTS `moyi_user_avatar`;
        #CREATE TABLE `moyi_user_avatar` (
        #        `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
        #        `username` varchar(255) NOT NULL,
        #        `phone` varchar(255) NOT NULL,
        #        `address` varchar(255) NOT NULL,
        #        `contact_id` varchar(255) NOT NULL,
        #        `avatar_data` text NOT NULL,
        #        `avatar_resize_s` mediumblob NOT NULL,
        #        PRIMARY KEY (`id`),
        #        UNIQUE KEY `username` (`username`)
        #        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        #
        # table_define = {
        #       'table_name' : 'user_contact',
        #       'table_primary_key' : ['user_id', 'contact_id'],
        #       'table_indexs' : [{'query_by_phone':['phone']},{'query_by_phone_address':['phone','address']}],
        #       'table_uniques' : [{'unique_username':['username']},{'unique_contact_id':['contact_id']}],
        #       'table_fields' : [
        #           ('`user_id`', 'int(10) unsigned', 'NOT NULL', 'AUTO_INCREMENT'),
        #           ('`username`', 'varchar(255)', 'NOT NULL'),
        #           ('`phone`', 'varchar(255)', 'NOT NULL'),
        #           ('`address`', 'varchar(255)', 'NOT NULL'),
        #           ('`contact_id`', 'varchar(255)', 'NOT NULL'),
        #           ('`avatar_data`', 'text', 'NOT NULL'),
        #           ('`avatar_resize_s`', 'mediumblob', 'NOT NULL'),
        #       ],
        #       'sharding_needed' : False,
        #       'sharding_method' : 'SegmentSharding',
        #       'sharding_seg_key' : 'user_id',
        #       'sharding_seg_per_table' : 100000,
        #       'sharding_seg_table_num' : 10,
        # }
        table_names = []
        range_num = 0
        sql = ""
        if table_define['sharding_needed'] :
            if 'SegmentSharding' == table_define['sharding_method'] :
                for i in range(0, table_define['sharding_seg_table_num']) :
                    table_names.append("%s_%d" % (table_define['table_name'], i))
                    range_num = table_define['sharding_seg_table_num']
            elif 'DateSharding' == table_define['sharding_method'] :
                start_date = table_define['sharding_start_date']
                if start_date:
                    try:
                        start_dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    except:
                        start_dt = datetime.datetime.now()
                else:
                    start_dt = datetime.datetime.now()
                for i in range(0, table_define['sharding_date_table_num']) :
                    dt = start_dt + datetime.timedelta(days=i)
                    table_names.append("%s_%s" % (table_define['table_name'], dt.strftime("%Y_%m_%d")))
                range_num = table_define['sharding_date_table_num']
            elif 'TimeVersionSharding' == table_define['sharding_method'] :
                # create meta
                sql = ("DROP TABLE IF EXISTS `%s_table_meta`;" % table_define['table_name']) + self.__GEN_LINE_BREAK
                sql += ("CREATE TABLE `%s_table_meta` (" % table_define['table_name']) + self.__GEN_LINE_BREAK
                sql += (" `%s` varchar(255) NOT NULL DEFAULT ''," % 'table_name') + self.__GEN_LINE_BREAK
                sql += (" `%s` text NOT NULL," % 'meta_object') + self.__GEN_LINE_BREAK
                sql += (" `%s` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'," % 'insert_time') + self.__GEN_LINE_BREAK
                sql += (" `%s` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'," % 'update_time') + self.__GEN_LINE_BREAK
                sql += ("PRIMARY KEY (`%s`)" % 'table_name') + self.__GEN_LINE_BREAK
                sql += ") ENGINE=InnoDB DEFAULT CHARSET=utf8;" + self.__GEN_LINE_BREAK
                # insert init meta data
                meta_dict = {}
                for (k,v) in table_define['sharding_time_interval'].items() :
                    meta_dict[k] = {}
                    meta_dict[k]['start_time'] = 0
                    meta_dict[k]['count'] = 0
                    meta_dict[k]['last_create_time'] = 0
                meta_object = json.dumps(meta_dict)
                sql += ("INSERT INTO `%s_table_meta` (`table_name`,`meta_object`) VALUES('%s', '%s');" % (table_define['table_name'], table_define['table_name'], meta_object)) + self.__GEN_LINE_BREAK
                sql += self.__GEN_LINE_BREAK
                sql += self.__GEN_LINE_BREAK
                table_names.append(table_define['table_name'])
                range_num = 1
            elif 'ConsistentHashSharding' == table_define['sharding_method'] :
                range_num = table_define['sharding_ch_table_num']
                for i in range(0, range_num) :
                    table_names.append("%s_%d" % (table_define['table_name'], i))
        else :
            table_names.append(table_define['table_name'])
            range_num = 1

        for i in range(0, range_num) :
            if i > 0:
                sql += ("CREATE TABLE `%s` like `%s`;" % (table_names[i], table_names[0])) + self.__GEN_LINE_BREAK
                continue
            sql += ("CREATE TABLE `%s` (" % table_names[i]) + self.__GEN_LINE_BREAK
            #table field
            for field in table_define['table_fields'] :
                line = ""
                for v in field :
                    line += (" %s" % v)
                sql += ("%s," % line) + self.__GEN_LINE_BREAK
            #primary key
            line = ""
            for v in table_define['table_primary_key'] :
                line += " `%s`," % v
            line = line.rstrip(",")
            sql += ("PRIMARY KEY (%s)," % line) + self.__GEN_LINE_BREAK
            #index
            if table_define.has_key('table_indexes') :
                for index in table_define['table_indexes'] :
                    line = "INDEX %s (" % index.items()[0][0]
                    for v in index.items()[0][1] :
                        line += (" `%s`," %v)
                    line = line.rstrip(",") + ")"

                    sql += ("%s, " % line) + self.__GEN_LINE_BREAK
            #uniqe
            if table_define.has_key('table_uniques') :
                for index in table_define['table_uniques'] :
                    line = "UNIQUE %s (" % index.items()[0][0]
                    for v in index.items()[0][1] :
                        line += (" `%s`," %v)
                    line = line.rstrip(",") + ")"

                    sql += ("%s, " % line) + self.__GEN_LINE_BREAK
            sql = sql.rstrip()
            sql = sql.rstrip(",") + self.__GEN_LINE_BREAK
            if 'utf8' == self._charset :
                sql += ") ENGINE=InnoDB DEFAULT CHARSET=utf8;  " + self.__GEN_LINE_BREAK
            elif 'utf8mb4' == self._charset :
                sql += ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;  " + self.__GEN_LINE_BREAK
            sql += self.__GEN_LINE_BREAK
        return sql

    def _insert_table(self, table_name, insert_param):
        self._change_to_master()
        input_param = {
            'table_name': table_name,
            'field_values': insert_param,
        }
        timestamp = int(time.time())
        if 'insert_time' not in insert_param :
            input_param['field_values']['insert_time'] = timestamp
        if 'update_time' not in insert_param :
            input_param['field_values']['update_time'] = timestamp
        sql = self._gen_insert_sql(input_param)
        logging.debug('the insert sql[%s]' % sql)

        insertid = -1
        try:
            res = self._db_cursor.execute(sql)
            insertid = self._db_conn.insert_id()
        except Exception, e:
            logging.error(
                'insert mysql failed! exception[%s] sql[%s]' % (e, sql), exc_info=True)
            return None

        if 0 == insertid:
            insertid = -1
        return insertid

    def _select_table(self, table_name, select_param, limit=None, order_by=None, fields=None, **kwargs):
        # get database
        self._get_db()


        select_param = {
            'table_name': table_name,
            'where': select_param,
        }
        select_param.update(kwargs)
        if fields :
            select_param['fields'] = fields
        else :
            select_param['fields'] = self._table_define[table_name]['table_fields_key']

        if limit :
            select_param['limit'] = limit
        if order_by :
            select_param['order_by'] = order_by
        sql = self._gen_select_sql(select_param)
        logging.debug('the select sql[%s]' % sql)

        row = {}
        try:
            res = self._db_cursor.execute(sql)
            row = self._db_cursor.fetchallDict()
        except Exception, e:
            logging.error(
                'select mysql failed! exception[%s] sql[%s]' % (e, sql), exc_info=True)
            return None
        return row

    def _update_table_by_key(self, table_name, keys, update_param, affected_row=False):
        self._change_to_master()

        input_param = {
            'table_name': table_name,
            'field_values': update_param,
            'where': keys,
        }
        if 'update_time' not in update_param :
            input_param['field_values']['update_time'] = int(time.time())
        sql = self._gen_update_sql(input_param)
        logging.debug('the update sql[%s]' % sql)

        res = 0
        try:
            res = self._db_cursor.execute(sql)
        except Exception, e:
            logging.warning(
                'update mysql failed! exception[%s] sql[%s]' % (e, sql))
            return False
        if affected_row == True:
            return res
        else:
            return True

    def _delete_table_by_key(self, table_name, keys):
        self._change_to_master()

        delete_param = {
            'table_name': table_name,
            'where': keys,
        }
        sql = self._gen_delete_sql(delete_param)
        logging.debug('the delete sql[%s]' % sql)

        res = 0
        try:
            res = self._db_cursor.execute(sql)
        except Exception, e:
            logging.warning(
                'delete mysql failed! exception[%s] sql[%s]' % (e, sql))
            return False
        return True

    def _query_table(self, sql) :
        sql = sql.strip()
        self._change_to_master()
        logging.debug('the query sql[%s]' % sql)
        try:
            res = self._db_cursor.execute(sql)
            return res
        except Exception, e:
            logging.warning(
                'query mysql failed! exception[%s] sql[%s]' % (e, sql))
            return None

    def fetch_table(self, sql, cursor_cls=MySQLdb.cursors.SSDictCursor):
        logging.debug("the fetch query[%s]", sql)
        try:
            _db_conn, db = self.__get_db_conn(need_master=True)
            _db_conn.query("set net_read_timeout=86400")
            _cursor = _db_conn.cursor(cursor_cls)
            _cursor.execute(sql)
            ct = 0
            while True:
                row = _cursor.fetchone()
                if not row:
                    break
                yield row
                ct += 1
            logging.info("fetch table finish[sql: %s, rows: %d]", sql, ct)
        except Exception as e:
            logging.warning(
                'fetch mysql failed! exception[%s] sql[%s]' % (e, sql))

    def escape_string(self, v):
        return self._db_conn.escape_string(v.encode("utf8"))
