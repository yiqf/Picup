"""
Time:     2023/4/11 8:31
Author:   忆千峰
Version:  V 0.1
File:     base.py
Email:    yiqf2022@126.com
"""
import time
from threading import Thread

from PySide2 import QtCore, QtWidgets

from picup.compress.base import CompressBase
from picup.ui.custom_inner import MyFonts
from picup.ui.custom_outer import RepUi


class Base:

    def __init__(self, scale_rate, icon, version):

        self._ui = RepUi(icon)

        self._ui.setupUi(scale_rate, version)
        self._ui.setWindowIcon(icon)
        self._ui.setWindowFlags(
            QtCore.Qt.FramelessWindowHint
        )

        self._ui.bclose.clicked.connect(self._ui.quit_app)
        self._ui.btask.clicked.connect(self._ui.hide)
        self._ui.bmin.clicked.connect(self._ui.showMinimized)

        self._ui.compress_button_group.setId(self._ui.compress_close, 0)
        self._ui.compress.setStretch(1, 1)
        close_name = self._ui.compress_close.text()
        self._compress_mapping = {0: (close_name, None, self._ui.compress_close)}
        self._ui.compress.setStretch(1, len(close_name.encode("gbk")))
        sub_cls = get_all_subclasses(CompressBase)
        if sub_cls:
            for index, cls in enumerate(sub_cls):
                obj = cls()
                button_id = index + 1
                button_name = obj.name
                custom_compress = QtWidgets.QRadioButton(self._ui.widget)
                font = MyFonts()
                font.setFamily("方正行黑简体")
                font.setPointSize(14)
                custom_compress.setFont(font)
                custom_compress.setObjectName(button_name)
                custom_compress.setText(button_name)
                self._ui.compress_button_group.addButton(custom_compress)
                self._ui.compress_button_group.setId(custom_compress, button_id)
                self._ui.compress.addWidget(custom_compress)
                self._ui.compress.setStretch(button_id + 1, len(button_name.encode("gbk")))

                self._compress_mapping[button_id] = (button_name, obj.compress_image_obj, custom_compress)

        self._ui.rename_button_group.setId(self._ui.rename_close, 0)
        self._ui.rename_button_group.setId(self._ui.rename_open, 1)

        self._step = 0
        self.pool = []

    def _get_ui_message(self):
        return {
            "address": self._ui.address_edit.text(),
            "username": self._ui.username_edit.text(),
            "password": self._ui.password_edit.text(),
            "custom_link": self._ui.custom_link_edit.text(),
            "compress": self._ui.compress_button_group.checkedId(),
            "rename": self._ui.rename_button_group.checkedId(),
            "rename_text": self._ui.rename_open_edit.text()
        }

    def _is_enabled(self, step):
        """
        校验当前步是否需要执行
        """
        return True if step == self._step and self._ui.run_flag else False

    def _blocking_wait(self, step):
        """
        等待线程执行，即只保留最新的线程
        """
        while len(self.pool) > 1 and self._is_enabled(step):
            for i in range(len(self.pool) - 2, -1, -1):
                if not self.pool[i].is_alive():
                    self.pool.pop(i)
        return True if self._is_enabled(step) else False

    def _parallel_run(self, target, *args):
        """
        以多线程方式启动
        """
        self._step += 1
        message = self._get_ui_message()
        self.pool.append(Thread(target=target, args=(self._step, message, *args)))
        if self._blocking_wait(self._step): self.pool[-1].start()

    @staticmethod
    def _add_time(s):
        return "{} : {}".format(time.strftime('%Y-%m-%d %H:%M:%S'), s)


def get_all_subclasses(cls: object, subclasses_list: list = []):
    sub_classes = cls.__subclasses__()
    for sub_class in sub_classes:
        if sub_class not in subclasses_list:
            subclasses_list.append(sub_class)
            get_all_subclasses(sub_class, subclasses_list)
    return subclasses_list
