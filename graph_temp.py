import sys
import time
import os

from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import*
from PyQt5 import uic
from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#hello


FROM_CLASS_MainWindow = uic.loadUiType("graph_temp.ui")[0]

class MainWindow(QMainWindow, FROM_CLASS_MainWindow):
    def __init__(self, temp_list, x, y):
        super().__init__()
        self.setupUi(self)
        self.move(x,y)
        self.temp_list = list(temp_list)
        x = [i for i in range(len(temp_list))]
        self.setWindowFlags(self.windowFlags())
        self.Graph1.setYRange(0, 50)
        self.Graph1.plot(x, temp_list)
        self.Graph1.setBackground('w')
        self.Graph2.setBackground('w')
        self.Graph1.showGrid(x=True, y=True)
        self.Graph2.showGrid(x=True, y=True)

        self.Thread_temp = My_Threed(self)
        self.Thread_temp.start()
        self.Thread_temp.user_signal.connect(self.temp_sig)

    def closeEvent(self, QCloseEvent):
        self.Thread_temp.is_running = False
    
    @pyqtSlot(float)
    def temp_sig(self,j):
        self.temp_list.append(j)
        x = [i for i in range(len(self.temp_list))]
        self.Graph1.plot(x, self.temp_list,pen=pg.mkPen('r', width=1))
        self.Graph2.setYRange(0, 60)
        self.Graph2.setXRange(x[len(x) - 1] - 30, x[len(x) - 1]+10)
        self.Graph2.plot(x, self.temp_list, pen=pg.mkPen('r', width=1))
        self.label_2.setText("현재 온도 값 그래프 (현재 온도 : {})".format(self.temp_list[len(x) - 1]))

'''def plot_temp(self, hour, temperature):
        pen_2 = pg.mkPen('r', width=2)
        self.Graph2.setYRange(0, 60)
        self.Graph2.setXRange(self.count_number - 30, self.count_number+10)
        
    
    def plot_hum(self, hour, temperature):
        pen_1 = pg.mkPen('b', width=2)
        self.Graph1.setYRange(0, 100)
        self.Graph1.setXRange(self.count_number - 30, self.count_number+10)
        self.Graph1.plot(hour, temperature, pen = pen_1)'''



class My_Threed(QThread):
    user_signal = pyqtSignal(float)
    
    def __init__(self, parent):
        super().__init__(parent)

    def run(self):
        self.is_running = True
        while(self.is_running):
            print("1")
            ref = db.reference('temp')
            self.user_signal.emit(ref.get())
            time.sleep(0.5)
        print("종료")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    ShowApp = MainWindow()
    ShowApp.show()
    
    print("끝")
    app.exec_()
    
    