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


class Webdav:
    clients = {}

    @classmethod
    def get_client(cls, address, username, password):
        key = (address, username, password)
        if key in cls.clients:
            return cls.clients[key]
        else:
            client = Client(address, auth=(username, password))
            cls.clients[key] = client
            return client

    @classmethod
    def upload_file(cls, filepath, data):
        client = cls.get_client(f"{data['address']}", data["username"], data["password"])
        _, filename = os.path.split(filepath)
        if client.exists(filename):
            raise UploadException(f"{filename}已存在，请稍后再试")
        client.upload_file(filepath, filename)
        return f"{data['custom_link']}/{filename}"

    @classmethod
    def upload_file_obj(cls, fp, filename, data):
        client = cls.get_client(f"{data['address']}", data["username"], data["password"])
        if client.exists(filename):
            raise UploadException(f"{filename}已存在，请稍后再试")
        client.upload_fileobj(fp, filename)
        return f"{data['custom_link']}/{filename}"
