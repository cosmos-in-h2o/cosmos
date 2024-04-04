from PyQt6.QtWidgets import QWidget
from PyQt6 import QtGui, QtCore
from qfluentwidgets import PlainTextEdit

import ui.settingui as sui


class Setting(QWidget, sui.Ui_Setting):
    def __init__(self, conf, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
