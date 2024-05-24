import sys
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import*
from PyQt5 import uic
from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

#hello


FROM_CLASS_MainWindow = uic.loadUiType("graph_hum.ui")[0]

class MainWindow(QMainWindow, FROM_CLASS_MainWindow):
    def __init__(self,hum_list,x,y):
        super().__init__()
        self.setupUi(self)
        self.move(x,y)
        self.Graph1.setBackground('w')
        self.Graph2.setBackground('w')
        self.hum_list = list(hum_list)
        x = [i for i in range(len(hum_list))]
        self.setWindowFlags(self.windowFlags())
        self.Graph1.setYRange(0, 50)
        self.Graph1.plot(x, hum_list)
        self.Graph1.showGrid(x=True, y=True)
        self.Graph2.showGrid(x=True, y=True)
        self.Thread_hum = My_Threed(self)
        self.Thread_hum.start()
        self.Thread_hum.user_signal.connect(self.hum_sig)
        
        



    def closeEvent(self, QCloseEvent):
        self.Thread_hum.is_running = False

    def hum_sig(self, j):
        self.hum_list.append(j)
        x = [i for i in range(len(self.hum_list))]

        self.Graph1.plot(x, self.hum_list,pen=pg.mkPen('b', width=1))
        self.Graph2.setYRange(0, 60)
        self.Graph2.setXRange(x[len(x) - 1] - 30, x[len(x) - 1]+10)
        self.Graph2.plot(x, self.hum_list, pen=pg.mkPen('b', width=1))
        self.label_2.setText("현재 습도 값 그래프 (현재 습도 : {})".format(self.hum_list[len(x) - 1]))

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    ShowApp = MainWindow()
    ShowApp.show()
    app.exec_()


class My_Threed(QThread):
    user_signal = pyqtSignal(float)
    
    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        self.is_running = True
        while(self.is_running):
            print("1")
            ref = db.reference('hum')
            self.user_signal.emit(ref.get())
            time.sleep(0.5)
        print("종료")
    
