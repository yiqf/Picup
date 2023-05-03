"""
Time:     2023/4/24 20:25
Author:   忆千峰
Version:  V 0.1
File:     public.py
Email:    yiqf2022@126.com
"""
import os.path
from enum import Enum
from types import DynamicClassAttribute


class ResEnum(Enum):
    
    SUCCESS = ("0000", "操作已完成")
    PASS = ("0001", "压缩率小于设定值，跳过压缩....")

    
    FAILED = ("9999", "操作失败")

    
    OVERFLOW = ("9110", "too many requests")

    @DynamicClassAttribute
    def code(self):
        return self.value[0]

    @DynamicClassAttribute
    def message(self):
        return self.value[1]


class CompressDataDto:
    """
    二进制文件压缩返回
    """
    success: bool = False
    code: str = None
    error_message: str = ""  
    source_data: bytes = None
    source_size: int = None
    target_data: bytes = None
    target_size: int = None
    ratio: float = 1


class CompressPathDto(CompressDataDto):
    """
    文件路径压缩返回
    """
    source_path: str = None
    target_path: str = None

    def __init__(self, source_path, target_path):
        self.source_path = os.path.abspath(source_path)
        self.target_path = os.path.abspath(target_path)

    def copy_from_data(self, dto: CompressDataDto):
        if isinstance(dto, CompressDataDto):
            self.__dict__.update(dto.__dict__)


def get_data_writeable(dto: CompressDataDto) -> bytes:
    """
    校验图片压缩是否成功
    :param dto: 压缩返回实体类
    :return:
    """
    if dto.code == ResEnum.SUCCESS.code:
        target_data = dto.target_data
    elif dto.code == ResEnum.PASS.code:
        target_data = dto.source_data
    else:
        target_data = None
    return target_data


def compress_image(compress_method: callable,
                   source_path: str, target_path: str, compress: float = 0.1,
                   *args, **kwargs) -> CompressPathDto:
    """
    输入文件名压缩指定文件
    :param compress_method: 压缩函数
    :param source_path: 源文件路径
    :param target_path: 目标文件路径
    :param compress: 最小有效压缩率
    """
    path_dto = CompressPathDto(source_path, target_path)
    try:
        with open(source_path, 'rb') as f:
            source_data = f.read()
        data_dto: CompressDataDto = compress_method(source_data, compress, *args, **kwargs)
        path_dto.copy_from_data(data_dto)
        target_data = get_data_writeable(data_dto)  
        if target_data:
            with open(target_path, 'wb') as f:
                f.write(target_data)
    except Exception as e:
        path_dto.code = ResEnum.FAILED.code
        path_dto.error_message = f"上传失败 {e.__class__.__name__}"
    finally:
        return path_dto
