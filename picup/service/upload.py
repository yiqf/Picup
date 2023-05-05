"""
Time:     2023/4/12 0:35
Author:   忆千峰
Version:  V 0.1
File:     upload.py
Email:    yiqf2022@126.com
"""
import os
import re
from tempfile import TemporaryFile

import pyperclip
import requests

from picup.compress.public import CompressDataDto
from picup.service.base import Base
from picup.storage import webdav


class Upload(Base):

    def __init__(self, *args, **kwargs):
        super(Upload, self).__init__(*args, **kwargs)

    def _upload_with_path(self, step, data, filepath):
        """
        按文件路径上传
        """
        if not os.path.exists(filepath):
            self._ui.upload_text.setText("文件不存在！")
        elif not os.path.isfile(filepath):
            self._ui.upload_text.setText("请上传文件对象！")
        else:
            with open(filepath, "rb") as fp:
                _, ext = os.path.splitext(filepath)
                self._upload_with_obj(step, fp, ext.lower(), data)

    def _upload_with_obj(self, step, fp, ext, data):
        """
        拖拽进入，按文件对象上传
        """

        compress_message = ""
        compress_button_id = data["compress"]
        if compress_button_id != 0:
            button_name, compress_obj, _ = self._compress_mapping[compress_button_id]
            self._ui.upload_text.setText(f"图片压缩中({button_name})，请稍候...")
            img_data = fp.read()
            dto: CompressDataDto = compress_obj(img_data, compress=0)
            if dto.success:
                compress_message = f"{button_name} : {dto.source_size / 1024:.2f}kb->{dto.target_size / 1024:.2f}kb ratio:{dto.ratio:.4f}"
                self._ui.upload_text.setText(f"{compress_message}")
                compress_message += "\n"
            else:
                self._ui.upload_text.setText(f"{dto.error_message}")
                return
            fp = TemporaryFile()
            fp.write(dto.target_data)
            fp.seek(0)

        if not self._is_enabled(step): return

        self._ui.upload_text.setText(f"{compress_message}正在上传...")
        try:
            custom_link = webdav.upload_file_obj(fp, ext, data)
            fp.close()
            self._ui.upload_url.setText(custom_link)
            pyperclip.copy(custom_link)
            self._ui.upload_text.setText(f"{compress_message}{self._add_time(f'上传成功！')}")
        except Exception as e:
            self._ui.upload_text.setText(f"上传失败，请检查网络和参数配置！\n{e.__class__.__name__}")

    def _upload_with_url(self, step, data, url):
        if url.startswith("http"):
            self._ui.upload_text.setText(f"图片读取中({url})...")
            result = re.search(r".*(\.[^\.]*$)", url.split("?")[0])
            ext = result.group(1) if result else ""
            fp = None
            try:
                response = requests.get(url, timeout=100)
                fp = TemporaryFile()
                fp.write(response.content)
                fp.seek(0)
            except Exception as e:
                self._ui.upload_text.setText(f"图片读取失败 {e.__class__.__name__}")
            if fp: self._upload_with_obj(step, fp, ext, data)
        else:
            self._ui.upload_text.setText(f"请传入url,当前输入\n{url}")
