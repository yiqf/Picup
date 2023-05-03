"""
Time:     2023/4/10 9:30
Author:   忆千峰
Version:  V 0.1
File:     webdav.py
Email:    yiqf2022@126.com
"""
import os
import uuid
from datetime import datetime

from webdav4.client import Client


def upload_file(filepath, data):
    client = Client(f"{data['address']}{data['path']}", auth=(data["username"], data["password"]))
    _, ext = os.path.splitext(filepath)
    filename = gen_safe_filename(client, ext, data["rename_text"])
    client.upload_file(filepath, filename)
    return f"{data['custom_link']}/{filename}"


def upload_file_obj(fp, ext, data):
    client = Client(base_url=data['address'], auth=(data["username"], data["password"]))
    filename = gen_safe_filename(client, ext, data["rename_text"])
    client.upload_fileobj(fp, filename)
    return f"{data['custom_link']}/{filename}"


def gen_safe_filename(client: Client, ext: str, rename_text) -> str:
    if not rename_text: rename_text = '%Y%m%d%H%M%S-{uuid}'
    now_str = datetime.strftime(datetime.now(), rename_text)  
    filename = f"{now_str}{ext}"
    filename = filename.format(uuid=uuid.uuid4().hex)
    while client.exists(filename):
        now_str = datetime.strftime(datetime.now(), rename_text)
        filename = f"{now_str}{ext}".replace("{uuid}", uuid.uuid4().hex)
    return filename
