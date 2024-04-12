import sys
import time
from point_move import MainWindow as mw
from error import MainWindow as er_mw
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import*
from PyQt5 import uic
try:
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import db
except:
    error_mw = er_mw("인터넷 연결오류",1)
    error_mw.show()

from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg


FROM_CLASS_MainWindow = uic.loadUiType("untitled.ui")[0]

class MainWindow(QMainWindow,FROM_CLASS_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lcdNumber_2.display(0)
        
        self.Thread_ = My_Threed(self)
        self.Thread_.start()
        self.Graph1.setBackground('w')
        self.Graph2.setBackground('w')
        self.Graph1.showGrid(x=False, y=True)
        self.Graph2.showGrid(x=False, y=True)
        self.Thread_.user_temp.connect(self.button_emit_temp)
        self.Thread_.user_hum.connect(self.button_emit_hum)

        self.pushButton.clicked.connect(self.activate)
        self.pushButton_2.clicked.connect(self.activate_2)

        self.Graph1.plot([-100,1000000],[55,55],pen = pg.mkPen('b',width=2,dash=[2, 4]))
        

    def activate_2(self):
        self.error_mw = er_mw("인터넷 연결오류",1)
        self.error_mw.show()
    
    def activate(self):
        x = self.frameGeometry().x()
        y = self.frameGeometry().y()
        print(x)
        self.point_move_ui = mw(x,y)
        self.point_move_ui.show()

    def plot_temp(self, hour, temperature):
        pen_2 = pg.mkPen('r', width=2)
        self.Graph2.setYRange(0, 60)
        self.Graph2.setXRange(self.count_number - 30, self.count_number+10)
        self.Graph2.plot(hour, temperature, pen = pen_2)
    
    def plot_hum(self, hour, temperature):
        pen_1 = pg.mkPen('b', width=2)
        self.Graph1.setYRange(0, 100)
        self.Graph1.setXRange(self.count_number - 30, self.count_number+10)
        self.Graph1.plot(hour, temperature, pen = pen_1)
    
    temp = [0,0,0,0,0,0,0,0,0,0]
    hum = [0,0,0,0,0,0,0,0,0,0]
    count = [1,2,3,4,5,6,7,8,9,10]
    count_number = 10

    temp_error = False
    hum_error = False

    @pyqtSlot(int)
    def button_emit_temp(self, i):
        self.lcdNumber_4.display(i)
        self.lcdNumber_3.display(sum(self.temp)/10)
        del self.temp[0]
        self.temp.append(i)
        del self.count[0]
        self.count_number += 1
        self.count.append(self.count_number)
        self.plot_temp(self.count,self.temp)


    
    def button_emit_hum(self, i):
        if((i > 55) and self.hum_error == False):
            self.hum_error = True
            self.error_mw = er_mw("습도 기준치 초과", 1)
            self.error_mw.show()
        if((self.hum_error == True) and i < 50):
            self.hum_error = False
        self.lcdNumber_2.display(i)
        self.lcdNumber.display(sum(self.hum)/10)
        del self.hum[0]
        self.hum.append(i)
        self.plot_hum(self.count,self.hum)

class My_Threed(QThread):
    user_temp = pyqtSignal(int)
    user_hum = pyqtSignal(int)
    def __init__(self, parent):
        super().__init__(parent)


    def run(self):
        self.is_running = True
        self.hum = 0
        self.temp = 0
        ref = db.reference("move_start")
        self.check = ref.get()
        time_save = time.time()
        while(self.is_running):
            if(0.5 < time.time() - time_save):
                ref = db.reference('temp')
                self.temp = ref.get()
                ref = db.reference('hum')
                self.hum = ref.get()
                self.user_temp.emit(self.temp)
                self.user_hum.emit(self.hum)
                    
                    
             
    def stop(self):
        self.is_running = False


app = QApplication(sys.argv)
ShowApp = MainWindow()
ShowApp.show()
app.exec_()