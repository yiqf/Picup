"""
Time:     2023/4/10 9:39
Author:   忆千峰
Version:  V 0.1
File:     custom_outer.py
Email:    yiqf2022@126.com
对完整ui进行继承附加操作
"""

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QMenu

from picup.ui.main_form import Ui_Form


class RepUi(Ui_Form):
    def __init__(self, icon):
        super(RepUi, self).__init__()

        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(icon)
        self.menu = QMenu()

        self.menu.addAction(QAction('显示', self.tray_icon, triggered=self.show_ahead))
        self.menu.addAction(QAction('隐藏', self.tray_icon, triggered=self.hide))
        self.menu.addAction(QAction('退出', self.tray_icon, triggered=self.quit_app))

        self.tray_icon.activated.connect(self.act)
        self.tray_icon.setContextMenu(self.menu)

        self.Flag = False
        self.mouse_x = None
        self.mouse_y = None
        self.origin_x = None
        self.origin_y = None

        self._paste_method = None

        self.run_flag = True

    def act(self, reason):

        if reason == 2:
            if self.isVisible() and not self.isMinimized():
                self.hide()
            else:
                self.show()
                self.showNormal()

    def quit_app(self):

        self.run_flag = False
        self.show()
        self.tray_icon.setVisible(False)
        QCoreApplication.instance().quit()

    def show_ahead(self):
        self.show()
        self.activateWindow()
        self.showNormal()

    def set_paste_method(self, paste_method):
        self._paste_method = paste_method

    def keyPressEvent(self, keyevent):
        modifiers = keyevent.modifiers()
        if modifiers == QtCore.Qt.ControlModifier and keyevent.key() == 86:
            if self._paste_method: self._paste_method()

    def mousePressEvent(self, evt):

        if evt.button() == QtCore.Qt.LeftButton:
            self.Flag = True
            self.mouse_x = evt.globalX()
            self.mouse_y = evt.globalY()

            self.origin_x = self.x()
            self.origin_y = self.y()

    def mouseMoveEvent(self, evt):
        if self.Flag:
            move_x = evt.globalX() - self.mouse_x
            move_y = evt.globalY() - self.mouse_y
            dest_x = self.origin_x + move_x
            dest_y = self.origin_y + move_y
            self.move(dest_x, dest_y)

    def mouseReleaseEvent(self, QMouseEvent):
        self.Flag = False

    def closeEvent(self, event) -> None:
        self.tray_icon.setVisible(False)
        self.run_flag = False
