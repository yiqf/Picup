"""
Time:     2023/5/1 23:31
Author:   忆千峰
Version:  V 0.1
File:     base.py
Email:    yiqf2022@126.com
"""
from abc import abstractmethod
from picup.compress.public import CompressDataDto, CompressPathDto


class CompressBase:
    """
    如果需要开启图片压缩，请继承此类，并重写compress_image_obj方法
    注意，需要设置name属性，标识压缩功能名称，不然可能无法使用
    """

    name = ""

    def __init__(self):
        pass

    @abstractmethod
    def compress_image_obj(self, source_data: bytes, compress: float = 0.1) -> CompressDataDto:
        pass

    def compress_image(self, source_path: str, target_path: str, compress: float = 0.1,
                       *args, **kwargs) -> CompressPathDto:
        pass

    @property
    def name(self):
        return self.name
