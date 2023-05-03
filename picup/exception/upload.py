"""
Time:     2023/5/1 23:02
Author:   忆千峰
Version:  V 0.1
File:     upload.py
Email:    yiqf2022@126.com
"""


class UploadException(Exception):
    def __init__(self, *args, **kwargs):
        super(UploadException, self).__init__(*args, **kwargs)
