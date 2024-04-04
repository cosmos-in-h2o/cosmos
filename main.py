import os
import sys

import jsonpickle
from PyQt6.QtWidgets import QApplication, QWidget
from qfluentwidgets import SplitFluentWindow, FluentIcon, NavigationItemPosition

# 子界面
import commander
import home
import setting

import config


class MyWindow(SplitFluentWindow):
    def __init__(self, conf, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Cosmos")

        # 子界面
        self.commander = commander.Commander(conf, parent=self)
        self.home = home.Home(conf, parent=self)
        self.setting = setting.Setting(conf, parent=self)
        self.addSubInterface(self.home, FluentIcon.HOME, "主页", NavigationItemPosition.TOP)
        self.addSubInterface(self.commander, FluentIcon.COMMAND_PROMPT, "命令行", NavigationItemPosition.TOP)
        self.addSubInterface(self.setting, FluentIcon.SETTING, "设置", NavigationItemPosition.BOTTOM)


if __name__ == "__main__":
    os.environ["QT_FONT_DPI"] = "100"
    conf = config.loadConfig()
    config.saveConfig(conf)
    print(jsonpickle.dumps(conf))
    app = QApplication(sys.argv)
    # 创建窗口
    window = MyWindow(conf)
    window.show()
    app.exec()
