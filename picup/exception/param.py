"""
Time:     2023/5/1 23:01
Author:   忆千峰
Version:  V 0.1
File:     param.py
Email:    yiqf2022@126.com
"""


class ParamException(Exception):
    def __init__(self, *args, **kwargs):
        super(ParamException, self).__init__(*args, **kwargs)
