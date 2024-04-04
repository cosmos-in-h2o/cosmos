import sys
#coding:utf-8
from PyQt6 import QtWidgets
from PyQt6.QtCore import *
from PyQt6.Qsci import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import re
import keyword
import os
'''感谢https://blog.csdn.net/xiaoyangyang20/article/details/68923133?fps=1&locationNum=4
，https://blog.csdn.net/tgbus18990140382/article/details/26136661
，https://qscintilla.com
。'''

class highlight(QsciLexerPython):
    def __init__(self,parent):
        QsciLexerPython.__init__(self,parent)
        font = QFont()
        font.setFamily('Courier')
        font.setPointSize(12)
        font.setFixedPitch(True)
        self.setFont(font)
        self.setColor(QColor(0, 0, 0))
        self.setPaper(QColor(255, 255, 255))
        self.setColor(QColor("#00FF00"), QsciLexerPython.ClassName)
        self.setColor(QColor("#B0171F"), QsciLexerPython.Keyword)
        self.setColor(QColor("#00FF00"), QsciLexerPython.Comment)
        self.setColor(QColor("#FF00FF"), QsciLexerPython.Number)
        self.setColor(QColor("#0000FF"), QsciLexerPython.DoubleQuotedString)
        self.setColor(QColor("#0000FF"), QsciLexerPython.SingleQuotedString)
        self.setColor(QColor("#288B22"), QsciLexerPython.TripleSingleQuotedString)
        self.setColor(QColor("#288B22"), QsciLexerPython.TripleDoubleQuotedString)
        self.setColor(QColor("#0000FF"), QsciLexerPython.FunctionMethodName)
        self.setColor(QColor("#191970"), QsciLexerPython.Operator)
        self.setColor(QColor("#000000"), QsciLexerPython.Identifier)
        self.setColor(QColor("#00FF00"), QsciLexerPython.CommentBlock)
        self.setColor(QColor("#0000FF"), QsciLexerPython.UnclosedString)
        self.setColor(QColor("#FFFF00"), QsciLexerPython.HighlightedIdentifier)
        self.setColor(QColor("#FF8000"), QsciLexerPython.Decorator)
        self.setFont(QFont('Courier',12,weight=QFont.Bold),5)
        self.setFont(QFont('Courier',12,italic=True),QsciLexerPython.Comment)

class MainWindow(QMainWindow):
    def __init__(self,parent=None,title='未命名',filenamearg=None):
        super(MainWindow,self).__init__(parent)
        self.setGeometry(100,100,1000,700)
        self.setWindowTitle(title)
        font=QFont()
        font.setFamily('Courier')
        font.setPointSize(12)
        font.setFixedPitch(True)
        self.setFont(font)
        self.editor=QsciScintilla()
        self.editor.setFont(font)
        self.setCentralWidget(self.editor)
        self.editor.setUtf8(True)
        self.editor.setMarginsFont(font)
        self.editor.setMarginWidth(0,len(str(len(self.editor.text().split('\n'))))*20)
        self.editor.setMarginLineNumbers(0,True)

        self.editor.setEdgeMode(QsciScintilla.EdgeLine)
        self.editor.setEdgeColumn(80)
        self.editor.setEdgeColor(QColor(0,0,0))

        self.editor.setBraceMatching(QsciScintilla.StrictBraceMatch)

        self.editor.setIndentationsUseTabs(True)
        self.editor.setIndentationWidth(4)
        self.editor.setTabIndents(True)
        self.editor.setAutoIndent(True)
        self.editor.setBackspaceUnindents(True)
        self.editor.setTabWidth(4)

        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor('#FFFFCD'))

        self.editor.setIndentationGuides(True)

        self.editor.setFolding(QsciScintilla.PlainFoldStyle)
        self.editor.setMarginWidth(2,12)

        self.editor.markerDefine(QsciScintilla.Minus, QsciScintilla.SC_MARKNUM_FOLDEROPEN)
        self.editor.markerDefine(QsciScintilla.Plus, QsciScintilla.SC_MARKNUM_FOLDER)
        self.editor.markerDefine(QsciScintilla.Minus, QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.editor.markerDefine(QsciScintilla.Plus, QsciScintilla.SC_MARKNUM_FOLDEREND)

        self.editor.setMarkerBackgroundColor(QColor("#FFFFFF"), QsciScintilla.SC_MARKNUM_FOLDEREND)
        self.editor.setMarkerForegroundColor(QColor("#272727"), QsciScintilla.SC_MARKNUM_FOLDEREND)
        self.editor.setMarkerBackgroundColor(QColor("#FFFFFF"), QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.editor.setMarkerForegroundColor(QColor("#272727"),QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.editor.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.editor.setAutoCompletionCaseSensitivity(True)
        self.editor.setAutoCompletionReplaceWord(False)
        self.editor.setAutoCompletionThreshold(1)
        self.editor.setAutoCompletionUseSingle(QsciScintilla.AcusExplicit)
        self.lexer=highlight(self.editor)
        self.editor.setLexer(self.lexer)
        self.mod=False
        self.__api = QsciAPIs(self.lexer)
        autocompletions = keyword.kwlist+["abs", "all", "any", "basestring", "bool",
                "callable", "chr", "classmethod", "cmp", "compile",
                "complex", "delattr", "dict", "dir", "divmod",
                "enumerate", "eval", "execfile", "exit", "file",
                "filter", "float", "frozenset", "getattr", "globals",
                "hasattr", "hex", "id", "int", "isinstance",
                "issubclass", "iter", "len", "list", "locals", "map",
                "max", "min", "object", "oct", "open", "ord", "pow",
                "property", "range", "reduce", "repr", "reversed",
                "round", "set", "setattr", "slice", "sorted",
                "staticmethod", "str", "sum", "super", "tuple", "type",
                "vars", "zip",'print']
        for ac in autocompletions:
            self.__api.add(ac)
        self.__api.prepare()
        self.editor.autoCompleteFromAll()
        if filenamearg:
            obj=open(filenamearg,'r+',encoding='utf-8')
            try:
                self.editor.setText(obj.read())
            except:
                QMessageBox.warning(self,'警告','无法打开此文件！',QMessageBox.Ok)
                self.editor.document().clear()
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        fileNewAction = self.createAction("新建",self.newfile,
                                          'Ctrl+N', "filenew", "创建Python文件")
        fileOpenAction = self.createAction("打开", self.fileopen,
                                           'Ctrl+O', "fileopen",
                                           "打开Python文件")
        self.fileSaveAction = self.createAction("保存", self.save,
                                                'Ctrl+S', "filesave", "保存Python文件")
        self.fileSaveAsAction = self.createAction("另存为",
                                                  self.saveas,None,
                                                  "用新名字保存文件")
        fileQuitAction = self.createAction("退出", self.close,
                                           "Ctrl+Q", "filequit", "退出")
        self.editCopyAction = self.createAction("撤销",
                                                self.editor.undo,'Ctrl+Z', "editcopy",
                                                "撤销")
        self.editCutAction = self.createAction("重做", self.editor.redo,
                                               'Ctrl+Alt+Z', "editcut",
                                               "重做")
        self.findAction = self.createAction("查找",
                                                self.findtext, 'Ctrl+F', "editcopy",
                                                "查找")
        self.replaceAction = self.createAction("替换", None,
                                               'Ctrl+R', "editcut",
                                               "替换")
        self.runAction = self.createAction('运行',self.run,'Ctrl+B','','运行程序')
        fileMenu = self.menuBar().addMenu("文件")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                                   self.fileSaveAction, self.fileSaveAsAction, None,
                                   fileQuitAction))
        editMenu = self.menuBar().addMenu("编辑")
        self.addActions(editMenu, (self.editCopyAction,
                                   self.editCutAction,  None,self.findAction,self.replaceAction))
        runMenu=self.menuBar().addMenu('运行')
        self.addActions(runMenu,(self.runAction,))
        self.name=''
        self.editor.textChanged.connect(self.changed)
        self.filename=filenamearg
    def run(self):
        if self.windowTitle()=='未命名':
            self.askforsave()
        print(self.windowTitle())
        os.system('call python '+self.windowTitle())
    def changed(self):
        self.mod=True
        self.editor.setMarginWidth(0, len(str(len(self.editor.text().split('\n')))) * 20)
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
    def askforsave(self):
        if self.mod:
            r=QMessageBox.question(self,'询问','是否要保存?',QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if r==QMessageBox.Cancel:
                return False
            elif r==QMessageBox.Yes:
                return self.save()
            return True
    def save(self):
        if not self.name:
            return self.saveas()
        self.mod=False
        self.setWindowTitle(self.name)
        obj=open(self.name,'w',encoding='utf-8')
        obj.truncate()
        obj.close()
        obj = open(self.name, 'r+', encoding='utf-8')
        try:
            obj.write(self.editor.text())
        except:
            obj.write('An error has occcured when trying to save this file.')
        obj.close()
    def saveas(self):
        filename,_buff=QFileDialog.getSaveFileName(self,'另存为','./','Python文件 (*.py)')
        if filename:
            self.name=filename
            return self.save()
        return False
    def newfile(self):
        if self.mod:
            if not self.askforsave():
                return -1
        self.editor.clear()
        self.mod=False
        self.name=''
        self.setWindowTitle('未命名')
    def fileopen(self):
        if self.mod:
            if not self.askforsave():
                return -1
        filename, _buff = QFileDialog.getOpenFileName(self, '另存为', './', 'Python文件 (*.py)')
        if filename:
            self.name = filename
            obj=open(self.name,'r+',encoding='utf-8')
            try:
                self.editor.setText(obj.read())
            except Exception as e:
                self.editor.setText("Can't read this file!Error:"+str(e))
            obj.close()
            self.setWindowTitle(self.name)
            self.mod=False
    def closeEvent(self, event):
        if not self.askforsave():
            event.ignore()
        event.accept()
    def findtext(self):
        pass

def main():
    import sys
    from os import path
    app = QApplication(sys.argv)
    fname = '未命名'
    if len(sys.argv) > 1:
        if path.isfile(sys.argv[1]):
            fname = sys.argv[1]
    form = MainWindow(None,fname,fname if fname!='未命名' else None)
    form.show()
    app.exec_()

main()