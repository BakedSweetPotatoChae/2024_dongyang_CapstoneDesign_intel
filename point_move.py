import sys
import time
from graph_hum import MainWindow as mw

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

        self.move_2.clicked.connect(self.move1_atuo)
        #self.move_3.clicked.connect(self.move2_atuo)
        #self.move_4.clicked.connect(self.move3_atuo)
        #self.move_5.clicked.connect(self.move4_atuo)
        
        #self.move_1.clicked.connect(self.move1)
        self.move_6.clicked.connect(self.move2)
        """self.move_9.clicked.connect(self.move3)
        self.move_8.clicked.connect(self.move4)"""
        

        self.frame.setLineWidth(2) # 굵기2로
        self.frame.setMidLineWidth(3) # 추가 굵기 3으로
        self.frame.setFrameShape(QFrame.Panel) # 형태는 Box로
        self.frame.setFrameShadow(QFrame.Raised)
        
        self.frame_2.setLineWidth(2) # 굵기2로
        self.frame_2.setMidLineWidth(3) # 추가 굵기 3으로
        self.frame_2.setFrameShape(QFrame.Panel) # 형태는 Box로
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.frame_3.setLineWidth(2) # 굵기2로
        self.frame_3.setMidLineWidth(3) # 추가 굵기 3으로
        self.frame_3.setFrameShape(QFrame.Panel) # 형태는 Box로
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.frame_4.setLineWidth(2) # 굵기2로
        self.frame_4.setMidLineWidth(3) # 추가 굵기 3으로
        self.frame_4.setFrameShape(QFrame.Panel) # 형태는 Box로
        self.frame_4.setFrameShadow(QFrame.Raised)
        
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

    """def move1(self):
        ref = db.reference()
        ref.update({"motor_move_1":True})
        ref.update({"move_start":True})
        ref = db.reference("move_start")"""

    def move2(self):
        ref = db.reference()
        ref.update({"motor_move_2":True})
        ref.update({"move_start":True})


    """def move3(self):
        ref = db.reference()
        ref.update({"motor_move_3":True})
        ref.update({"move_start":True})"""


    """def move4(self):
        ref = db.reference()
        ref.update({"motor_move_4":True})
        ref.update({"move_start":True})"""

    
   

    def move1_atuo(self):
        self.move_count_list = [self.label_1,self.label_54,self.label_56,self.label_56]
        self.move_save_start([1,2,3,4,0])


    """def move2_atuo(self):
        self.move_count_list = [self.label_45,self.label_47,self.label_49,self.label_49]
        self.move_save_start([1,3,2,4,0])"""


    """def move3_atuo(self):
        self.move_count_list = [self.label_38,self.label_40,self.label_42,self.label_42]
        self.move_save_start([1,4,2,3,0])"""


    """def move4_atuo(self):
        self.move_count_list = [self.label_33,self.label_32,self.label_35,self.label_35]
        self.move_save_start([4,3,2,1,0])"""

        
    motor_move_list = [[],[],[],[]]
    arrow = 0
    time_Save = 0
    move_timer_check = False
    def move_timer(self):
        self.move_timer_check = True
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
                self.move_timer_check = False
                self.move_count_list[self.cout_move_list_number].setText("->")
                self.cout_move_list_number += 1
                if(self.move_1_list[self.cout_move_list_number] == 0):
                    db.reference().update({"move_start":False})
                    self.timer.stop()

    sw_move_start = False
    
    @pyqtSlot(list)
    def button_emit_enabled_check(self, i):
        if(i[0]['move_start'] == True):
            self.main_move.setText("동작중")
            if(self.sw_move_start == False):
                style = """
                QFrame{
                    background-color:rgb(71,200,62)
                }"""
                self.sw_move_start = True
            else:
                style = """
                QFrame{
                    background-color:rgb(70,65,217)
                }"""
                self.sw_move_start = False
            self.main_move.setStyleSheet(style)
        else:
            self.main_move.setText("정지")
            style = """
            QFrame{
	            background-color:rgb(241,95,95)
            }"""
            self.main_move.setStyleSheet(style)
        if(i[1]['motor_1'] == True):
            self.motor_1.setText("동작중")
            style = """
            QFrame{
                background-color:rgb(71,200,62)
            }"""
            self.motor_1.setStyleSheet(style)
        else:
            self.motor_1.setText("정지")
            style = """
            QFrame{
	            background-color:rgb(241,95,95)
            }"""
            self.motor_1.setStyleSheet(style)
        if(i[2]['motor_2'] == True):
            self.motor_2.setText("동작중")
            style = """
            QFrame{
                background-color:rgb(71,200,62)
            }"""
            self.motor_2.setStyleSheet(style)
        else:
            self.motor_2.setText("정지")
            style = """
            QFrame{
	            background-color:rgb(241,95,95)
            }"""
            self.motor_2.setStyleSheet(style)
        if(i[3]['motor_3'] == True):
            self.motor_3.setText("동작중")
            style = """
            QFrame{
                background-color:rgb(71,200,62)
            }"""
            self.motor_3.setStyleSheet(style)
        else:
            self.motor_3.setText("정지")
            style = """
            QFrame{
	            background-color:rgb(241,95,95)
            }"""
            self.motor_3.setStyleSheet(style)
        if(i[4]['motor_4'] == True):
            self.motor_4.setText("동작중")
            style = """
            QFrame{
                background-color:rgb(71,200,62)
            }"""
            self.motor_4.setStyleSheet(style)
        else:
            self.motor_4.setText("정지")
            style = """
            QFrame{
	            background-color:rgb(241,95,95)
            }"""
            self.motor_4.setStyleSheet(style)

        if((time.time() - self.time_Save > 0.5)and(i[0]['move_start'] == True)):
            try:
                if((self.arrow == 0)and(self.move_timer_check == True)):

                    self.move_count_list[self.cout_move_list_number].setText(">")
                    self.arrow += 1
                elif(self.arrow == 1):

                    self.move_count_list[self.cout_move_list_number].setText(">>")
                    self.arrow += 1
                elif(self.arrow == 2):

                    self.move_count_list[self.cout_move_list_number].setText(">>>")
                    self.arrow = 0
            except(IndexError):
                print("인덱스 에러")
            self.time_Save = time.time()
    
    def closeEvent(self, QCloseEvent):
        self.Thread_.is_running = False



class My_Threed(QThread):
    user_signal = pyqtSignal(list)
    
    def __init__(self, parent):
        super().__init__(parent)


    def run(self):
        self.is_running = True
        user_move_point_list = ["move_start", "motor_1","motor_2","motor_3","motor_4"]
        user_move_point = [{0:0} for i in range(5)]

        while(self.is_running):
            count = 0
            for i in user_move_point_list:
                ref = db.reference(i)
                user_move_point[count] = ({i:ref.get()})
                count += 1
            self.user_signal.emit(user_move_point)
            count = 0

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    ShowApp = MainWindow()
    ShowApp.show()
    app.exec_()
