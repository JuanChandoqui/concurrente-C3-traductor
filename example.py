from typing import Text
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
import time
import sys


class EmittingStream(QtCore.QObject):  
        textWritten = QtCore.pyqtSignal(str)  # defines a signal that sends str 
        def write(self, data):
            self.textWritten.emit(str(data)) 

class BackendThread(QThread):
     #  a signal is defined by a class member object 
    update_date = pyqtSignal(str)

     #  process business logic 
    def run(self):
        while True:           
            self.update_date.emit(str("text"))
            time.sleep(1)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        
        # now redirect the output to textedit 
        sys.stdout = EmittingStream(textWritten=self.handleDisplay)  
        sys.stderr = EmittingStream(textWritten=self.handleDisplay)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", " real-time display "))
        self.pushButton.setText(_translate("MainWindow", " start "))

    def initUI(self):
          #  create a thread 
        self.backend = BackendThread()
          #  connect the signal 
        self.backend.update_date.connect(self.handleDisplay)
          #  to start a thread 
        self.backend.start()

    #  prints the current time to the text box 
    def handleDisplay(self, data):
        cursor = self.textEdit.textCursor()  
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(data)  
        self.textEdit.setTextCursor(cursor)  
        self.textEdit.ensureCursorVisible()

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    win = Ui_MainWindow()
    win.setupUi(MainWindow)
    win.initUI()
    MainWindow.show()
    sys.exit(app.exec_())