#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import csv
import logging
import re

from utils.mysql.models.base_model import *

class FileDownloadModel(object):
    
    file_writer = None
    TMP_FILE_PATH = '/tmp/exportmodel.tmp'

    def __init__(self, file_path = None):
        if file_path != None:
            self.TMP_FILE_PATH = file_path


    def write_data_to_file(self, data):
        try:
            with open(self.TMP_FILE_PATH, 'w') as file_write:
                self.file_writer = csv.writer(file_write)
                self.file_writer.writerows(data)
            
            file_write.close()

            logging.info("Writing data to file `%s` successfully ..." % self.TMP_FILE_PATH)
            return True

        except Exception as e:
            logging.warning('Writing data to file `%s` unsuccessfully ... \nError message : %s' % (self.TMP_FILE_PATH, e))
            return False

    def read_data_from_file(self):
        try:
            with open(self.TMP_FILE_PATH, 'r') as file_read:
                file_data = file_read.read()

            file_read.close()

            logging.info("Reading data from file `%s` successfully ..." % self.TMP_FILE_PATH)
            return file_data

        except Exception as e:
            logging.warning('Reading data from file `%s` unsuccessfully ... \nError message : %s' % (self.TMP_FILE_PATH, e))
            return False


class FileUploadHandler(object):

    FILE_METAS = None
    UPLOAD_PATH = None
    FILE_MAX_SIZE = 5 * 1024 * 1024
    FILE_TYPE = None
    FILE_VALIDATION = False

    def __init__(self, upload_path = None, files = None, _type = None, max_size = None):
        if upload_path == None:
            upload_path = '../static/uploads'
        
        if max_size != None:
            self.FILE_MAX_SIZE = max_size

        try:
            self.UPLOAD_PATH = os.path.join(os.path.dirname(__file__), upload_path)
            self.FILE_METAS = files.get('file', None)
            self.FILE_TYPE = _type
            self.validate_file()

        except Exception as e:
            logging.info('Initial file model unsuccessfully ... \nError message : %s' % e)
        
    def validate_file(self):
        
        isMAtchFileSize = True
        for meta in self.FILE_METAS:
            
            isMatchFileType = True
            if self.FILE_TYPE != None:
                if re.search(self.FILE_TYPE, meta['content_type']) == None:
                    isMatchFileType = False

            if len(meta.body) > self.FILE_MAX_SIZE:
                isMAtchFileSize = False
                break
        
        if isMatchFileType and isMAtchFileSize:
            self.FILE_VALIDATION = True
        else:
            self.FILE_VALIDATION = False

    def upload_file(self):
        
        try:
            for meta in self.FILE_METAS:
                filename = meta['filename']
                file_path = os.path.join(self.UPLOAD_PATH, filename)

                with open(file_path, 'wb') as file_upload:
                    file_upload.write(meta['body'])
            
            logging.info('File `%s` uploaded successfully ... ' % file_path )
            return filename
        except Exception as e:
            logging.info('File `%s` uploaded unsuccessfully ... \nError message : %s' % ( file_path, e ))
            return False