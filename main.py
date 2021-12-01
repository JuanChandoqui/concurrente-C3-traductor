#import libraries PyQt5
#import the name of the file from designer 
import sys
from PyQt5.QtCore import  QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic, QtCore 
import time
from Models import traslation


text, language_selected = '', ''

class EmittingStream(QtCore.QObject):  
        textWritten = QtCore.pyqtSignal(str)  # defines a signal that sends str 
        
        def write(self, data):
            self.textWritten.emit(str(data)) 

class BackendThread(QThread):
     #  a signal is defined by a class member object 
    update_date = pyqtSignal(str)

     #  process business logic 
    def run(self):
        global text, language_selected
        while True:
            try:
                input_text = traslation.translate_text(text, language_selected)     
                self.update_date.emit(str(input_text))
                time.sleep(0.1)
            except:
                sys.stdout.write('Vacio...')
            
            
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./Views/init.ui', self)
        self.button_exit.clicked.connect(self.close)
         # now redirect the output to textedit 
        sys.stdout = EmittingStream(textWritten=self.handleDisplay)  
        sys.stderr = EmittingStream(textWritten=self.handleDisplay)

    def handleDisplay(self, data):
        global text, language_selected
        language_selected = self.comboBox_languages.currentText()
        text = self.text_edit.toPlainText()
        cursor = self.show_translation.textCursor()  
        
        if text != "\n":
            self.show_translation.clear()
            self.show_translation.insertPlainText(data)
            self.show_translation.setTextCursor(cursor)  
    
    def initUI(self):
        self.backend = BackendThread()  #create a thread 
        self.backend.update_date.connect(self.handleDisplay)  #connect the signal 
        self.backend.start()
        
    def finishUI(self):
        self.backend.finished() #to finished


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Window()
    demo.initUI()
    demo.show()
    try: 
        sys.exit(app.exec_())
    except SystemExit:
        sys.stdout.write('Exit...')