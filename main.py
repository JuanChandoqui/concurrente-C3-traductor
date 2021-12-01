#import libraries PyQt5
#import the name of the file from designer 
import sys
from PyQt5.QtCore import  QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic, QtGui, QtCore 
import time

from Models import traslation
text = ''

class EmittingStream(QtCore.QObject):  
        textWritten = QtCore.pyqtSignal(str)  # defines a signal that sends str 
        def write(self, data):
            self.textWritten.emit(str(data)) 

class BackendThread(QThread):
     #  a signal is defined by a class member object 
    update_date = pyqtSignal(str)

     #  process business logic 
    def run(self):
        global text
        while True:
            input_text = traslation.translate_text(text)         
            self.update_date.emit(str(input_text))
            time.sleep(0.1)
            
            


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Views/init.ui', self)
        
         # now redirect the output to textedit 
        sys.stdout = EmittingStream(textWritten=self.handleDisplay)  
        sys.stderr = EmittingStream(textWritten=self.handleDisplay)

    def handleDisplay(self, data):
        global text
        input_text = self.text_edit.toPlainText()
        text = input_text
        self.show_translation.clear()
        cursor = self.show_translation.textCursor()  
        cursor.movePosition(QtGui.QTextCursor.End)
        self.show_translation.insertPlainText(data)
        self.show_translation.setTextCursor(cursor)  
        self.show_translation.ensureCursorVisible()
    
    def initUI(self):
        self.backend = BackendThread()  #create a thread 
        self.backend.update_date.connect(self.handleDisplay)  #connect the signal 
        self.backend.start() #to start a thread 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Window()
    demo.initUI()
    demo.show()

    try: 
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')