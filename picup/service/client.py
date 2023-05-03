"""
Time:     2023/4/11 8:30
Author:   忆千峰
Version:  V 0.1
File:     client.py
Email:    yiqf2022@126.com
"""
import os.path
from tempfile import TemporaryFile

import pyperclip
import requests
from PIL import ImageGrab, Image
from PySide2 import QtWidgets
from win32clipboard import OpenClipboard, GetClipboardData, CloseClipboard, CF_TEXT

from picup.service.config import Config
from picup.service.upload import Upload


class Client(Config, Upload):

    def __init__(self, scale_rate, icon, version):
        super(Client, self).__init__(scale_rate, icon, version)

        
        self._ui.file_source.set_drag(lambda filepath: self._parallel_run(self._drag_file, filepath))  
        self._ui.file_source.clicked.connect(self._choice_file)  
        self._ui.set_paste_method(lambda: self._parallel_run(self._paste_data))  
        self._ui.url_button.clicked.connect(lambda: self._parallel_run(self._clip_url))  
        self._ui.clip_button.clicked.connect(lambda: self._parallel_run(self._paste_data))  

        
        self._ui.paste_button.clicked.connect(self._paste_custom_link)

    def initialization(self):
        self._ui.activateWindow()
        self._get_config()

    def _paste_custom_link(self):
        """
        复制生成的链接
        """
        pyperclip.copy(self._ui.upload_url.text())

    def _choice_file(self):
        """
        选择文件上传
        """
        
        filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self._ui, "选取文件夹")
        self._parallel_run(self._upload_with_path, filepath)

    def _drag_file(self, step, data, filepath):
        """
        拖拽文件上传
        """
        try:
            self._upload_with_path(step, data, filepath)
        except Exception as e:
            self._ui.upload_text.setText(f"拖拽文件上传出错 \n{e.__class__.__name__}")

    def _clip_url(self, step, data):
        """
        上传剪切板中的url数据
        """
        content = ""
        self._ui.upload_text.setText(f"尝试获取剪切板信息...")
        try:
            OpenClipboard()
            content = GetClipboardData(CF_TEXT).decode('GBK')  
            CloseClipboard()
        except TypeError:  
            CloseClipboard()
            self._ui.upload_text.setText("获取剪切板链接信息失败，请检查剪切板！")
            return
        except Exception as e:
            self._ui.upload_text.setText(f"获取剪切板链接信息异常 {e.__class__.__name__}")
            return
        if not content:
            self._ui.upload_text.setText("剪切板为空,请检查剪切板！")
            return

        elif content.startswith("http"):  
            self._upload_with_url(step=step, data=data, url=content)
        else:  
            self._ui.upload_text.setText(f"剪切板信息不为链接,操作失败\n{content}")

    def _paste_data(self, step, data):
        """
        上传剪切板数据
        """
        content = ""
        self._ui.upload_text.setText(f"尝试获取剪切板信息...")
        try:
            OpenClipboard()
            content = GetClipboardData(CF_TEXT).decode('GBK')  
            CloseClipboard()
        except TypeError:  
            CloseClipboard()
            im = ImageGrab.grabclipboard()
            if isinstance(im, Image.Image):  
                im.convert('RGB')
                fp = TemporaryFile()
                im.save(fp, format="JPEG")
                fp.seek(0)
                self._upload_with_obj(step=step, fp=fp, ext=".jpg", data=data)
            elif isinstance(im, list):  
                self._upload_with_path(step=step, data=data, filepath=im[0])
            else:
                self._ui.upload_text.setText(f"获取剪切板信息失败，未知格式！ {type(im)}")
            return
        except Exception as e:
            self._ui.upload_text.setText(f"获取剪切板文本信息异常 {e.__class__.__name__}")
            return

        if not content:
            self._ui.upload_text.setText("剪切板为空,请检查剪切板！")
            return
        elif content.startswith("http"):  
            self._upload_with_url(step=step, data=data, url=content)
        else:  
            self._upload_with_path(step=step, data=data, filepath=content)

    def show(self):
        """ 窗口显示函数 """
        self._ui.show()
        self._ui.tray_icon.show()
        self.initialization()
