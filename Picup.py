"""
Time:     2022/01/06 0:10
Author:   忆千峰
Version:  V 0.1
File:     Picup.py
Email:    yiqf2022@126.com
"""
import os
import sys

import PyQt5

from picup.service import client
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

if __name__ == '__main__':
    __version__ = "2.2.1"

    app = QApplication(sys.argv)
    scaleRate = app.screens()[0].logicalDotsPerInch() / 120
    icon = QIcon("resource/icons/Picup.svg")
    win = client.Client(scaleRate, icon, __version__)
    win.show()
    sys.exit(app.exec_())
