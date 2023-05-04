"""
Time:     2023/5/1 23:31
Author:   忆千峰
Version:  V 0.1
File:     base.py
Email:    yiqf2022@126.com
"""
import requests
from abc import abstractmethod
from picup.compress.public import CompressPathDto, CompressDataDto, CompressException


class CompressBase:
    """
    如果需要开启图片压缩，请继承此类，并重写compress_image_obj方法
    注意，需要设置name属性，标识压缩功能名称，不然可能无法使用
    """

    _name = ""

    def __init__(self):
        pass

    @abstractmethod
    def compress_image_obj(self, source_data: bytes, compress: float = 0.1) -> CompressDataDto:
        pass

    def compress_image(self, source_path: str, target_path: str, compress: float = 0.1,
                       *args, **kwargs) -> CompressPathDto:
        pass

    @staticmethod
    def download_to_buffer(download_url: str, *args, **kwargs):
        try:
            res = requests.get(download_url)
            return res.content
        except Exception as e:
            raise CompressException(f"图片回传异常 {e.__class__.__name__}")

    @property
    def name(self):
        return self._name
