"""
Time:     2023/4/10 9:22
Author:   忆千峰
Version:  V 0.1
File:     custom_inner.py
Email:    yiqf2022@126.com
ui内部各组件的自定义操作
"""
import os.path
import re
import threading
import time
from datetime import datetime

from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QPushButton, QLabel

from picup import fonts_path


class MyQLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super(MyQLabel, self).__init__(*args, **kwargs)
        self._lock = threading.Lock()
        self._step = 0
        self.min_interval = 0.1

    def setText(self, arg__1: str):
        """
        多线程运行，避免影响主线程
        """
        self._step += 1
        threading.Thread(target=self.setTextBlocking, args=(arg__1, self._step)).start()

    def setTextBlocking(self, arg__1: str, step):
        """
        重写setText函数，防止过快写入导致的程序报错
        """
        self._lock.acquire()
        if step == self._step:
            super(MyQLabel, self).setText(arg__1)
            time.sleep(self.min_interval)
        self._lock.release()


class MyPushButton(QPushButton):
    """
    按键拖拽文件上传功能
    """

    def __init__(self, *args, **kwargs):
        super(MyPushButton, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self._drag = None

    def dragEnterEvent(self, event):

        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        res = re.search("file:///(.*)", event.mimeData().text())
        if res and self._drag:
            self._drag(res.group(1))

    def set_drag(self, drag):
        self._drag = drag


class MyFonts(QFont):
    """
    自定义字体
    请将字体文件保存在{fonts_path}下，并命名为{arg__1}.ttf
    """

    def __init__(self):
        super(MyFonts, self).__init__()

    def setFamily(self, arg__1):
        font_path = f"{fonts_path}/{arg__1}.ttf"
        if os.path.exists(font_path):
            id = QFontDatabase.addApplicationFont(font_path)
            fontstr = QFontDatabase.applicationFontFamilies(id)[0]

            super(MyFonts, self).setFamily(fontstr)
        else:
            print(f"缺少字体{arg__1}")
            super(MyFonts, self).setFamily(arg__1)
