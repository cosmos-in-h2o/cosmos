from PyQt6.QtWidgets import QWidget
from PyQt6 import QtGui, QtCore
from qfluentwidgets import PlainTextEdit

import ui.commanderui as cui
from commander_text import CommanderText


class Commander(QWidget, cui.Ui_Commander):
    def __init__(self, conf, parent=None):
        super().__init__(parent=parent)
        self.conf = conf
        self.setupUi(self)
        self.CommandTextEdit = CommanderText(conf, parent=self)
        self.CommandTextEdit.setObjectName("CommandTextEdit")
        self.verticalLayout.addWidget(self.CommandTextEdit)

        # 信号槽连接
        self.CommandTextEdit.returnPressed.connect(self.runCommand)

    def runCommand(self, text):
        # 内置命令处理
        if text == "clear":
            self.CommandTextEdit.clear()
            self.conf.user_name = "kurisu"
