#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import _mysql_exceptions
import sys
import os
from pprint import pprint
import new
import copy
import json
import time
import datetime
from weakref import proxy
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
    _table_define = {}

    _db_conn = None
    _db_is_master = False

    _db_list = []
    _db_conn_retry = 0
    _timeout = 10
    _charset = 'utf8'

    def __init__(self, db_list, db_conn_retry=3):
        for (k, v) in self._table_define.items():
            tmp = []
            for vv in v['table_fields']:
                tmp.append(vv[0])
            self._table_define[k]['table_fields_key'] = tmp[:]

        self._db_list = db_list
        self._db_conn_retry = db_conn_retry
        self._db_cursor = MyCursor(self)

    def __del__(self):
        self.__db_free()

    def db_free(self):
        self.__db_free()

    def __db_free(self):
        self._db_cursor.close()
        if None != self._db_conn:
            self._db_conn.close()
            self._db_conn = None

    def __get_db_conn(self, need_master):
        """
        get an database connection
        """
        # build mid
        i = 0
        for v in self._db_list:
            v['mid'] = str(i) + '_' + v['host'] + '_' + str(v['port'])
            i += 1
        # balance connected
        self.__db_free()
        bal = DBMasterSlaverRWBalance(self._db_list)

        db_conn = None
        db = None
        flag = False
        retry = self._db_conn_retry
        while retry > 0:
            try:
                db = bal.get_source({"need_master": need_master})
                logging.debug(
                    "balance get_resource get_db. host[%s] mid[%s]", db['host'], db['mid'])
                host = socket.gethostbyname(db['host'])
                db_conn = MySQLdb.connect(host=host, user=db['username'], passwd=db['password'],
                                          db=db['dbname'], charset=db['charset'], port=db['port'], connect_timeout=self._timeout)
                flag = True
                self._charset = db['charset']
            except Exception, e:
                logging.warning("connect to mysql failed. host[%s] mid[%s]. retry_remain[%d] e[%s]" % (
                    db['host'], db['mid'], retry, e), exc_info=True)
                bal.mask_failed(db["mid"])
            retry -= 1
            if flag:
                break
            time.sleep(3)

        if False == flag:
            logging.warning("Can not connect to mysql")
            return None, None
        return db_conn, db

    def _get_db(self):
        if None != self._db_conn:
            return self._db_conn

        self.__db_free()
        #init the database
        (self._db_conn, db) = self.__get_db_conn(need_master=False)
        if (None == self._db_conn):
            raise RuntimeError, "RuntimeError get db connection failed class[%s] __init__(self)" % self.__class__
        self._db_cursor.connect()
        if 'utf8mb4' == self._charset:
            self._db_cursor.execute("set names utf8mb4 collate utf8mb4_unicode_ci;")
        self._db_cursor.execute("set autocommit=1;")

        self._db_is_master = db['is_master']
        return self._db_conn

    def _gen_insert_sql(self, insert_param, need_escape=True):
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
        sql_keys = ''
        for v in insert_param['field_values'].keys():
            sql_keys += "`%s`," % v
        sql_keys = sql_keys.rstrip(',')
        sql += sql_keys + ") VALUES("
        sql_values = ''
        for v in insert_param['field_values'].values():
            sql_values += "%s," % self.__escape_string(v, need_escape)
        sql_values = sql_values.rstrip(',')
        sql += sql_values + ")"
        return sql

    def _gen_update_sql(self, update_param, need_escape=True):
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
        sql = 'UPDATE `%s` SET' % update_param['table_name']
        sql_set = ''
        for (k, v) in update_param['field_values'].items():
            sql_set += " `%s`=%s," % (k, self.__escape_string(v, need_escape))
        sql_set = sql_set.rstrip(',')
        sql += sql_set
        if 'str' == type(update_param['where']).__name__ or 'unicode' == type(update_param['where']).__name__:
            sql += " WHERE %s" % update_param['where']
        elif isinstance(update_param['where'], dict):
            sql += self.__gen_where(update_param['where'])
        else:
            sql = ''
        return sql

    def _gen_delete_sql(self, delete_param):
        """
        from a dict param to delete sql
        """
        sql = "DELETE FROM `%s`" % delete_param['table_name']
        if 'str' == type(delete_param['where']).__name__ or 'unicode' == type(delete_param['where']).__name__:
            sql += " WHERE %s" % delete_param['where']
        elif isinstance(delete_param['where'], dict):
            sql += self.__gen_where(delete_param['where'])
        else:
            sql = ''
        return sql

    def _gen_select_sql(self, select_param):
        """
        from a dict param to select sql
        """
        sql = "SELECT "
        sql_fields = ''
        for v in select_param['fields']:
            sql_fields += '%s,' % v
        sql += sql_fields.rstrip(',')
        sql += " FROM `%s`" % select_param['table_name']
        force_index = select_param.get('force_index', '')
        if '' != force_index:
            sql += ' FORCE INDEX(`%s`)' % force_index
        if 'str' == type(select_param['where']).__name__ or 'unicode' == type(select_param['where']).__name__:
            sql += " WHERE %s" % select_param['where']
        #if 'dict' == type(select_param['where']).__name__ :
        if isinstance(select_param['where'], dict) and {} != select_param['where']:
            sql += self.__gen_where(select_param['where'])
        if select_param.get('order_by'):
            order_by = select_param.get('order_by')
            sql += " ORDER BY %s" % order_by
        if select_param.get('limit'):
            (offset, count) = select_param.get('limit')
            sql += " limit %d, %d" % (offset, count)
        return sql

    def __gen_where(self, where_dict):
        tmp = " WHERE"
        flag = False
        for (k, v) in where_dict.items():
            if flag:
                tmp += " AND `%s`=" % (k)
            else:
                tmp += " `%s`=" % (k)
                flag = True
            tmp += self.__escape_string(str(v))
        return tmp

    def __escape_string(self, v, need_escape=True):
        """
        For the variable's type, escape it
        """
        if 'str' == type(v).__name__ or 'unicode' == type(v).__name__:
            if need_escape:
                return "'%s'" % self._db_conn.escape_string(v.encode("utf8"))
            else:
                return "'%s'" % v
        elif 'int' == type(v).__name__ or 'long' == type(v).__name__ or 'float' == type(v).__name__:
            return "%s" % v
        elif 'list' == type(v).__name__:
            return "%s" % v[0]
        else:
            return None

    def _insert_table(self, table_name, insert_param):
        self._change_to_master()
        input_param = {
            'table_name': table_name,
            'field_values': insert_param,
        }
        timestamp = int(time.time())
        if 'insert_time' not in insert_param:
            input_param['field_values']['insert_time'] = timestamp
        if 'update_time' not in insert_param:
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
        if fields:
            select_param['fields'] = fields
        else:
            select_param['fields'] = self._table_define[table_name]['table_fields_key']

        if limit:
            select_param['limit'] = limit
        if order_by:
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
        if 'update_time' not in update_param:
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

    def _query_table(self, sql):
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
