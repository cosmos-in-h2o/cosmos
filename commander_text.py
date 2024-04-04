from PyQt6.QtCore import pyqtSignal, Qt, QEvent
from PyQt6.QtGui import QTextCursor, QFont
from qfluentwidgets import TextEdit

import config


class CommanderText(TextEdit):
    returnPressed = pyqtSignal(str)

    def __init__(self, conf: config.Config, parent=None) -> None:
        super().__init__(parent)
        self.setTabStopDistance(40)
        self.setFont(QFont(conf.command_font.name, conf.command_font.size))
        self.conf = conf
        self.setText(f"{self.conf.user_name}>> ")
        self.flag_pos = self.document().characterCount() - 1  # 用于定向

    def keyPressEvent(self, event):
        is_ctrl = event.modifiers() & Qt.KeyboardModifier.ControlModifier
        if event.type() == QEvent.Type.KeyPress:
            if is_ctrl:
                if event.key() == Qt.Key.Key_V:
                    self.paste()
                elif event.key() == Qt.Key.Key_C:
                    self.copy()
                elif event.key() == Qt.Key.Key_X:
                    self.cut()
                else:
                    super().keyPressEvent(event)
            else:
                cursor = self.textCursor()
                if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                    # 获取要发送的文本并发送
                    if self.flag_pos != self.document().characterCount() - 1:
                        cursor = QTextCursor(self.document())
                        cursor.setPosition(self.flag_pos)
                        cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
                        self.returnPressed.emit(cursor.selectedText())
                    # 更新文本
                    self.append(f"{self.conf.user_name}>> ")
                    # 重置flag_pos
                    self.refreshFlagPos()
                    # 光标移动到末尾
                    cursor = self.textCursor()
                    cursor.movePosition(QTextCursor.MoveOperation.End)
                    self.setTextCursor(cursor)
                elif event.key() == Qt.Key.Key_Backspace or event.key() == Qt.Key.Key_Delete:
                    if cursor.hasSelection():
                        # 若末位都置于flag_pos之前，则不允许删除
                        if cursor.selectionEnd() <= self.flag_pos:
                            pass
                        # 末位置在flag_pos之后
                        else:
                            # 初位置在flag_pos之前
                            if cursor.selectionStart() < self.flag_pos:
                                # 重定选中位置并进行删除
                                temp_cursor = QTextCursor(self.document())
                                temp_cursor.setPosition(self.flag_pos)
                                temp_cursor.setPosition(cursor.selectionEnd(), QTextCursor.MoveMode.KeepAnchor)
                                self.setTextCursor(temp_cursor)
                            super().keyPressEvent(event)
                    else:
                        if cursor.position() - 1 >= self.flag_pos:
                            super().keyPressEvent(event)
                        else:
                            pass
                elif event.text():
                    if cursor.hasSelection():
                        # 若末位都置于flag_pos之前，则移动光标到末尾
                        if cursor.selectionEnd() <= self.flag_pos:
                            cursor.movePosition(QTextCursor.MoveOperation.End)
                            self.setTextCursor(cursor)
                        # 末位置在flag_pos之后
                        else:
                            # 初位置在flag_pos之前
                            if cursor.selectionStart() < self.flag_pos:
                                # 重定选中位置
                                temp_cursor = QTextCursor(self.document())
                                temp_cursor.setPosition(self.flag_pos)
                                temp_cursor.setPosition(cursor.selectionEnd(), QTextCursor.MoveMode.KeepAnchor)
                                self.setTextCursor(temp_cursor)
                    else:
                        if cursor.position() < self.flag_pos:
                            cursor.movePosition(QTextCursor.MoveOperation.End)
                            self.setTextCursor(cursor)
                    super().keyPressEvent(event)
                else:
                    super().keyPressEvent(event)

    # 中文输入法处理
    def inputMethodEvent(self, event):
        cursor = self.textCursor()
        if cursor.hasSelection():
            # 若末位都置于flag_pos之前，则移动光标到末尾
            if cursor.selectionEnd() <= self.flag_pos:
                cursor.movePosition(QTextCursor.MoveOperation.End)
                self.setTextCursor(cursor)
            # 末位置在flag_pos之后
            else:
                # 初位置在flag_pos之前
                if cursor.selectionStart() < self.flag_pos:
                    # 重定选中位置
                    temp_cursor = QTextCursor(self.document())
                    temp_cursor.setPosition(self.flag_pos)
                    temp_cursor.setPosition(cursor.selectionEnd(), QTextCursor.MoveMode.KeepAnchor)
                    self.setTextCursor(temp_cursor)
        else:
            if cursor.position() < self.flag_pos:
                cursor.movePosition(QTextCursor.MoveOperation.End)
                self.setTextCursor(cursor)
        super().inputMethodEvent(event)

    def paste(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            # 若末位都置于flag_pos之前，则粘贴到末尾
            if cursor.selectionEnd() <= self.flag_pos:
                cursor.movePosition(QTextCursor.MoveOperation.End)
                self.setTextCursor(cursor)
                super().paste()
            # 末位置在flag_pos之后
            else:
                # 初位置在flag_pos之前
                if cursor.selectionStart() < self.flag_pos:
                    # 重定选中位置
                    temp_cursor = QTextCursor(self.document())
                    temp_cursor.setPosition(self.flag_pos)
                    temp_cursor.setPosition(cursor.selectionEnd(), QTextCursor.MoveMode.KeepAnchor)
                    self.setTextCursor(temp_cursor)
                super().paste()
        else:
            if cursor.position() - 1 >= self.flag_pos:
                cursor.movePosition(QTextCursor.MoveOperation.End)
                self.setTextCursor(cursor)
                super().paste()
            else:
                pass

    def cut(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            # 若末位都置于flag_pos之前，则不剪切
            if cursor.selectionEnd() <= self.flag_pos:
                pass
            # 末位置在flag_pos之后
            else:
                # 初位置在flag_pos之前
                if cursor.selectionStart() < self.flag_pos:
                    # 重定选中位置
                    temp_cursor = QTextCursor(self.document())
                    temp_cursor.setPosition(self.flag_pos)
                    temp_cursor.setPosition(cursor.selectionEnd(), QTextCursor.MoveMode.KeepAnchor)
                    self.setTextCursor(temp_cursor)
                super().cut()
        else:
            if cursor.position() - 1 >= self.flag_pos:
                cursor.movePosition(QTextCursor.MoveOperation.End)
                self.setTextCursor(cursor)
                super().cut()
            else:
                pass

    def refreshFlagPos(self):
        self.flag_pos = self.document().characterCount() - 1
