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

#hello
cred = credentials.Certificate("C:/Users/대단한 승병이/Desktop/server_rel/wafer-stepmotor-firebase-adminsdk-foj75-3fc921b3c0.json")

firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://wafer-stepmotor-default-rtdb.firebaseio.com/'
})


FROM_CLASS_MainWindow = uic.loadUiType("move_set_ui.ui")[0]

class MainWindow(QMainWindow, FROM_CLASS_MainWindow):
    def __init__(self, x,y):
        super().__init__()
        self.setupUi(self)
        self.Thread_ = My_Threed(self)
        self.Thread_.start()
        self.setGeometry(x+1005,y+40,789,593)
        self.move_2.clicked.connect(self.move1_atuo)
        self.move_3.clicked.connect(self.move2_atuo)
        self.move_4.clicked.connect(self.move3_atuo)
        self.move_5.clicked.connect(self.move4_atuo)

        self.move_1.clicked.connect(self.move1)
        self.move_6.clicked.connect(self.move2)
        self.move_9.clicked.connect(self.move3)
        self.move_8.clicked.connect(self.move4)

        self.Thread_.user_signal.connect(self.button_emit_enabled_check)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_timer)
        self.move_1_list = [1,2,3,4]
        self.cout_move_list_number = 0
        self.cout_move_list_number_sw = False

    def move_save_start(self, move_list):
        ref = db.reference()
        ref.update({"move_start":True})
        self.move_1_list = move_list
        self.cout_move_list_number = 0
        self.cout_move_list_number_sw = False
        self.timer.start(10)

    def move1(self):
        ref = db.reference()
        ref.update({"motor_move_1":True})
        ref.update({"move_start":True})
        ref = db.reference("move_start")


    def move2(self):
        ref = db.reference()
        ref.update({"motor_move_2":True})
        ref.update({"move_start":True})
        print("2")

    def move3(self):
        ref = db.reference()
        ref.update({"motor_move_3":True})
        ref.update({"move_start":True})
        print("3")

    def move4(self):
        ref = db.reference()
        ref.update({"motor_move_4":True})
        ref.update({"move_start":True})
        print("4")
    
   

    def move1_atuo(self):
        self.move_save_start([1,2,3,4,0])
        print("1")

    def move2_atuo(self):
        self.move_save_start([1,3,2,4,0])
        print("2")

    def move3_atuo(self):
        self.move_save_start([1,4,2,3,0])
        print("3")

    def move4_atuo(self):
        self.move_save_start([4,3,2,1,0])
        print("4")
    

    def move_timer(self):
        ref = db.reference('move_start')
        (self.move_1_list[self.cout_move_list_number])
        if(self.move_1_list[self.cout_move_list_number] == 0 and self.cout_move_list_number_sw == False):
            db.reference().update({"move_start":False})
            self.timer.stop()
        if(self.cout_move_list_number_sw == False):
            db.reference().update({"motor_move_{}".format(str(self.move_1_list[self.cout_move_list_number])):True})
            db.reference().update({"move_start":True})
            self.cout_move_list_number_sw = True
        else:
            ref = db.reference('motor_move_{}'.format(str(self.move_1_list[self.cout_move_list_number])))
            if(ref.get() == False):
                self.cout_move_list_number_sw = False
                self.cout_move_list_number += 1
                if(self.move_1_list[self.cout_move_list_number] == 0):
                    db.reference().update({"move_start":False})
                    self.timer.stop()


    @pyqtSlot(bool)
    def button_emit_enabled_check(self, i):
        self.button_enabled(not i)
        print("a")
    
    def button_enabled(self, i):
        self.move_2.setEnabled(i)
        self.move_3.setEnabled(i)
        self.move_4.setEnabled(i)
        self.move_5.setEnabled(i)


        self.move_1.setEnabled(i)
        self.move_6.setEnabled(i)
        self.move_8.setEnabled(i)
        self.move_9.setEnabled(i)



class My_Threed(QThread):
    user_signal = pyqtSignal(bool)
    def __init__(self, parent):
        super().__init__(parent)


    def run(self):
        self.is_running = True
        ref = db.reference("move_start")
        self.check = ref.get()
        

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    ShowApp = MainWindow()
    ShowApp.show()
    app.exec_()
