"""
Time:     2023/4/10 9:30
Author:   忆千峰
Version:  V 0.1
File:     webdav.py
Email:    yiqf2022@126.com
"""
import os

from webdav4.client import Client

from picup.exception.upload import UploadException


def upload_file(filepath, data):
    client = Client(f"{data['address']}", auth=(data["username"], data["password"]))
    _, filename = os.path.split(filepath)
    if client.exists(filename):
        raise UploadException(f"{filename}已存在，请稍后再试")
    client.upload_file(filepath, filename)
    return f"{data['custom_link']}/{filename}"


def upload_file_obj(fp, filename, data):
    client = Client(base_url=data['address'], auth=(data["username"], data["password"]))
    if client.exists(filename):
        raise UploadException(f"{filename}已存在，请稍后再试")
    client.upload_fileobj(fp, filename)
    return f"{data['custom_link']}/{filename}"
