from PyQt6.QtWidgets import QWidget
import ui.homeui as hui


class Home(QWidget, hui.Ui_Home):
    def __init__(self, conf, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
