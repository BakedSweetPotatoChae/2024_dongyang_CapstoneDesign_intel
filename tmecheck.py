import sys
import time
from point_move import MainWindow as mw
from graph_hum import MainWindow as gr_hum_mw
from graph_temp import MainWindow as gr_temp_mw
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
        self.frame_3.setLineWidth(2) # 굵기2로
        self.frame_3.setMidLineWidth(3) # 추가 굵기 3으로
        self.frame_3.setFrameShape(QFrame.Panel) # 형태는 Box로
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.frame_6.setLineWidth(2) # 굵기2로
        self.frame_6.setMidLineWidth(3) # 추가 굵기 3으로
        self.frame_6.setFrameShape(QFrame.Panel) # 형태는 Box로
        self.frame_6.setFrameShadow(QFrame.Raised)

        self.frame_11.setLineWidth(2) # 굵기2로
        self.frame_11.setMidLineWidth(3 ) # 추가 굵기 3으로
        self.frame_11.setFrameShape(QFrame.Panel) # 형태는 Box로
        self.frame_11.setFrameShadow(QFrame.Raised)

        self.frame_18.setLineWidth(2) # 굵기2로
        self.frame_18.setMidLineWidth(3) # 추가 굵기 3으로
        self.frame_18.setFrameShape(QFrame.Panel) # 형태는 Box로
        self.frame_18.setFrameShadow(QFrame.Raised)
        
        self.frame_19.setLineWidth(2) # 굵기2로
        self.frame_19.setMidLineWidth(3) # 추가 굵기 3으로
        self.frame_19.setFrameShape(QFrame.Panel) # 형태는 Box로
        self.frame_19.setFrameShadow(QFrame.Raised)

        self.frame_16.setLineWidth(2) # 굵기2로
        self.frame_16.setMidLineWidth(3) # 추가 굵기 3으로
        self.frame_16.setFrameShape(QFrame.Panel) # 형태는 Box로
        self.frame_16.setFrameShadow(QFrame.Raised)

        self.frame_17.setLineWidth(2) # 굵기2로
        self.frame_17.setMidLineWidth(3) # 추가 굵기 3으로
        self.frame_17.setFrameShape(QFrame.Panel) # 형태는 Box로
        self.frame_17.setFrameShadow(QFrame.Raised)


        self.all_temp_save = [db.reference('hum').get()]
        self.all_hum_save = [db.reference('temp').get()]
        self.Thread_ = My_Threed(self)
        self.Thread_.start()
        
        '''self.Graph1.setBackground('w')
        self.Graph2.setBackground('w')
        self.Graph1.showGrid(x=True, y=True)
        self.Graph2.showGrid(x=True, y=True)'''
        self.Thread_.user_temp.connect(self.button_emit_temp)
        self.Thread_.user_hum.connect(self.button_emit_hum)
        
        self.pushButton.clicked.connect(self.activate)
        self.pushButton_2.clicked.connect(self.activate_2)
        '''
        '''
        self.hum_temp_table.setRowCount(100)
        self.hum_temp_table.setColumnCount(3)
        self.hum_wm_button.clicked.connect(self.gr_hum_mw_button_)
        self.temp_wm_button.clicked.connect(self.gr_temp_mw_button_)

        self.Thread_.user_signal.connect(self.button_emit_enabled_check)
        self.move_3.clicked.connect(self.move1_atuo)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_timer)
        self.move_1_list = [1,2,3,4]
        self.cout_move_list_number = 0
        self.cout_move_list_number_sw = False

    time_Save = 0


    def move_save_start(self, move_list):
        ref = db.reference()
        ref.update({"move_start":True})
        self.move_1_list = move_list
        self.cout_move_list_number = 0
        self.cout_move_list_number_sw = False
        self.timer.start(10)

        
    
    def gr_hum_mw_button_(self):
        x = self.frameGeometry().x() + self.frameGeometry().width()
        y = self.frameGeometry().y() 
        self.hum_mw = gr_hum_mw(self.all_hum_save,x,y)
        self.hum_mw.show()
    
    def gr_temp_mw_button_(self):
        x = self.frameGeometry().x() + self.frameGeometry().width()
        y = self.frameGeometry().y() + 640

        self.temp_mw = gr_temp_mw(self.all_temp_save, x,y)
        self.temp_mw.show()

    def progressBarValeue(self, value, ber_number):
        if(ber_number == 1 or ber_number == 2):
            styleSheet = """
            QFrame{
                border-radius: 90px;
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop: {STOP_2} rgba(85, 170, 255, 255));
            }"""
        else:
            styleSheet = """
            QFrame{
                border-radius: 90px;
                background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop: {STOP_2} rgba(204, 114, 61, 255));
            }"""

        progress = (100 - int(value)) / 100.0

        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)
        
        newStyleSheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}",stop_2)
        if(ber_number == 1):
            self.hum_number.setText(str(int(value)))
            self.cirylarBg_1.setStyleSheet(newStyleSheet)
        elif(ber_number == 2):
            self.cirylarBg_2.setStyleSheet(newStyleSheet)
            self.hum_number_2.setText(str(int(value)))
        elif(ber_number == 3):
            self.cirylarBg_3.setStyleSheet(newStyleSheet)
            self.hum_number_3.setText(str(int(value)))
        elif(ber_number == 4):
            self.cirylarBg_4.setStyleSheet(newStyleSheet)
            self.hum_number_4.setText(str(int(value)))

    def activate_2(self):
        self.error_mw = er_mw("인터넷 연결오류",1)
        self.error_mw.show()

    def activate(self):
        x = self.frameGeometry().x() - 1000
        y = self.frameGeometry().y() + int(self.frameGeometry().height()-1000)

        self.point_move_ui = mw(x,y)
        self.point_move_ui.show()


    
    count = [1,2,3,4,5,6,7,8,9,10]
    count_number = 10
    table_count = 1

    temp_error = False
    hum_error = False
    list_value_temp = [0 for i in range(30)]
    list_value_hum = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    all_temp_save = []
    all_hum_save = []
    temp_save = 0
    hum_save = 0
    temp_count = 0
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
    
    @pyqtSlot(float)
    def button_emit_temp(self, in_temp):
        self.button_emit_temp_check = True

        del self.list_value_temp[0]
        self.list_value_temp.append(in_temp)
        value = sum(self.list_value_temp)/30.0
        self.progressBarValeue(value,3)
        if((self.all_temp_save[len(self.all_temp_save)-1]+1<in_temp)or(self.all_temp_save[len(self.all_temp_save)-1]-1>in_temp)):
            self.progressBarValeue(in_temp,4)
            self.hum_temp_table.setItem( self.temp_count,0, QTableWidgetItem(str(time.strftime('%x,%X', time.localtime(time.time())))))
            self.hum_temp_table.setItem( self.temp_count,1, QTableWidgetItem("온도 변화 감지"))
            self.hum_temp_table.setItem( self.temp_count,2,QTableWidgetItem("{} -> {}".format(self.temp_save, in_temp)))
            self.temp_save = in_temp
            self.temp_count += 1
        self.all_temp_save.append(in_temp)

    def button_emit_hum(self, in_hum):
        if((in_hum > 55) and self.hum_error == False):
            self.hum_error = True
            self.error_mw = er_mw("습도 기준치 초과", 1)
            self.error_mw.show()
        if((self.hum_error == True) and in_hum < 50):
            self.hum_error = False
        del self.list_value_hum[0]
        self.list_value_hum.append(int(in_hum))
        value = sum(self.list_value_hum)/10.0
        self.progressBarValeue(value,1)
        if((self.all_hum_save[len(self.all_hum_save)-1]+1<in_hum)or(self.all_hum_save[len(self.all_hum_save)-1]-1>in_hum)):
            self.progressBarValeue(in_hum,2)    
            self.hum_temp_table.setItem( self.temp_count,0, QTableWidgetItem(str(time.strftime('%x,%X', time.localtime(time.time())))))
            self.hum_temp_table.setItem( self.temp_count,1, QTableWidgetItem("습도 변화 감지"))
            self.hum_temp_table.setItem( self.temp_count,2,QTableWidgetItem("{} -> {}".format(self.temp_save, in_hum)))
            self.temp_save = in_hum
            self.temp_count += 1
        self.all_hum_save.append(in_hum)

    
    def move1_atuo(self):
        self.move_count_list = [self.label_20,self.label_55,self.label_57,self.label_57]
        self.move_save_start([1,2,3,4,0])

    sw_move_start = False
    @pyqtSlot(list)
    def button_emit_enabled_check(self, i):
        if(i[0]['move_start'] == True):
            self.main_move_2.setText("동작중")
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
            self.main_move_2.setStyleSheet(style)
        else:
            self.main_move_2.setText("정지")
            style = """
            QFrame{
	            background-color:rgb(241,95,95)
            }"""
            self.main_move_2.setStyleSheet(style)
        if(i[1]['motor_1'] == True):
            self.motor_5.setText("동작중")
            style = """
            QFrame{
                background-color:rgb(71,200,62)
            }"""
            self.motor_5.setStyleSheet(style)
        else:
            self.motor_5.setText("정지")
            style = """
            QFrame{
	            background-color:rgb(241,95,95)
            }"""
            self.motor_5.setStyleSheet(style)
        if(i[2]['motor_2'] == True):
            self.motor_6.setText("동작중")
            style = """
            QFrame{
                background-color:rgb(71,200,62)
            }"""
            self.motor_6.setStyleSheet(style)
        else:
            self.motor_6.setText("정지")
            style = """
            QFrame{
	            background-color:rgb(241,95,95)
            }"""
            self.motor_6.setStyleSheet(style)
        if(i[3]['motor_3'] == True):
            self.motor_7.setText("동작중")
            style = """
            QFrame{
                background-color:rgb(71,200,62)
            }"""
            self.motor_7.setStyleSheet(style)
        else:
            self.motor_7.setText("정지")
            style = """
            QFrame{
	            background-color:rgb(241,95,95)
            }"""
            self.motor_7.setStyleSheet(style)
        if(i[4]['motor_4'] == True):
            self.motor_8.setText("동작중")
            style = """
            QFrame{
                background-color:rgb(71,200,62)
            }"""
            self.motor_8.setStyleSheet(style)
        else:
            self.motor_8.setText("정지")
            style = """
            QFrame{
	            background-color:rgb(241,95,95)
            }"""
            self.motor_8.setStyleSheet(style)

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
    user_temp = pyqtSignal(float)
    user_hum = pyqtSignal(float)
    user_signal = pyqtSignal(list)
    def __init__(self, parent):
        super().__init__(parent)


    def run(self):
        self.is_running = True
        self.hum = 0
        self.temp = 0
        ref = db.reference("move_start")
        self.check = ref.get()
        time_save = time.time()
        self.is_running = True
        user_move_point_list = ["move_start", "motor_1","motor_2","motor_3","motor_4"]
        user_move_point = [{0:0} for i in range(5)]
        while(self.is_running):
            if(0.1 < time.time() - time_save):
                ref = db.reference('temp')
                self.temp = ref.get()
                ref = db.reference('hum')
                self.hum = ref.get()
                self.user_temp.emit(self.temp)
                self.user_hum.emit(self.hum)
            count = 0
            for i in user_move_point_list:
                ref = db.reference(i)
                user_move_point[count] = ({i:ref.get()})
                count += 1
            self.user_signal.emit(user_move_point)
            count = 0
        
    def stop(self):
        self.is_running = False

app = QApplication(sys.argv)
ShowApp = MainWindow()
ShowApp.show()
app.exec_()