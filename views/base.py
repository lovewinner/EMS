#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado_lib.routes import route
from base_api_handler import BaseAPIHandler as BaseHandler

from models.file_model import FileDownloadModel
from models.file_model import FileUploadHandler

import csv
import json
import os
import logging

@route('/export_to_csv')
class Export2CSVHandler(BaseHandler):
    def get(self):
        data = [
            ('张三', '12岁', '自由职业'),
            ('李四', '14岁', '自由职业')
        ]

        file = FileDownloadModel()

        file.write_data_to_file(data)

        csv_data = file.read_data_from_file()

        self.set_header("Content-disposition", "attachment; filename='csv.csv'")
        self.write(csv_data)


@route('/upload_file')
class UploadHandler(BaseHandler):
    def get(self):
        self.write('''
            <html>
            <head><title>Upload File</title></head>
            <body>
                <form action='upload_file' enctype="multipart/form-data" method='post'>
                <input type='file' name='file'/><br/>
                <input type='submit' value='submit'/>
                </form>
            </body>
            </html>
        ''')

    def post(self):
        files = FileUploadHandler(files = self.request.files, _type = 'image')

        if files.FILE_VALIDATION:
            self.success(files.upload_file())
        else:
            self.failed({})