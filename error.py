import sys
import time

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import*
from PyQt5 import uic
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

FROM_CLASS_MainWindow = uic.loadUiType("error.ui")[0]

class MainWindow(QMainWindow, FROM_CLASS_MainWindow):
    def __init__(self, error_text_input, error_rating):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedHeight(330)
        self.setFixedWidth(521)
        self.exit_button.clicked.connect(self.close)
        qr = self.frameGeometry()
        self.cp_x = QDesktopWidget().availableGeometry().bottomRight().x()
        self.cp_y = QDesktopWidget().availableGeometry().bottomRight().y()
        self.i = self.cp_y
        self.error_text.setText(error_text_input)
        if(error_rating == 1):
            pal = QPalette()
            pal.setColor(QPalette.Background,QColor(255,0,255))
        self.move(self.cp_x-521,self.cp_y)
        time.sleep(0.5)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.moveWindow)
        self.timer.start(10)
        
        


    def moveWindow(self):

        self.cp_y -= 10
        self.move(self.cp_x-521, self.cp_y)
        if self.cp_y < self.i-300:
            self.timer.stop()

    




if __name__ == "__main__" :
    app = QApplication(sys.argv)
    ShowApp = MainWindow("인터넷 오류",1)
    ShowApp.show()
    app.exec_()
