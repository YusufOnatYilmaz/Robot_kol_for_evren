from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
import pyfirmata

board = pyfirmata.Arduino("COM3")
iter8 = pyfirmata.util.Iterator(board)
iter8.start()
pin6 = board.get_pin('d:6:s')
pin9 = board.get_pin('d:9:s')
pin10 = board.get_pin('d:10:s')
pin11 = board.get_pin('d:11:s')

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.value1 = 0
        self.value2 = 0
        self.value3 = 0
        self.value4 = 0
        self.position_1 = [90,90,90,90]
        self.position_2 = [90,90,90,90]
        self.go_there = True
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(822, 558)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.servo_1 = QtWidgets.QSlider(self.centralwidget)
        self.servo_1.setGeometry(QtCore.QRect(130, 90, 361, 41))
        self.servo_1.setMaximum(180)
        self.servo_1.setOrientation(QtCore.Qt.Horizontal)
        self.servo_1.setObjectName("servo_1")
        self.servo_2 = QtWidgets.QSlider(self.centralwidget)
        self.servo_2.setGeometry(QtCore.QRect(130, 170, 361, 41))
        self.servo_2.setMaximum(180)
        self.servo_2.setOrientation(QtCore.Qt.Horizontal)
        self.servo_2.setObjectName("servo_2")
        self.servo_3 = QtWidgets.QSlider(self.centralwidget)
        self.servo_3.setGeometry(QtCore.QRect(130, 250, 361, 41))
        self.servo_3.setMaximum(180)
        self.servo_3.setOrientation(QtCore.Qt.Horizontal)
        self.servo_3.setObjectName("servo_3")
        self.servo_4 = QtWidgets.QSlider(self.centralwidget)
        self.servo_4.setGeometry(QtCore.QRect(130, 330, 361, 41))
        self.servo_4.setMaximum(180)
        self.servo_4.setOrientation(QtCore.Qt.Horizontal)
        self.servo_4.setObjectName("servo_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(170, 400, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 400, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(170, 450, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(320, 450, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 822, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.servo_1.valueChanged.connect(self.pos)
        self.servo_2.valueChanged.connect(self.pos)
        self.servo_3.valueChanged.connect(self.pos)
        self.servo_4.valueChanged.connect(self.pos)

        self.servo_1.setMaximum(180)
        self.servo_2.setMaximum(180)
        self.servo_3.setMaximum(180)
        self.servo_4.setMaximum(180)

        self.pushButton.clicked.connect(self.go_pos_1)
        self.pushButton_2.clicked.connect(self.go_pos_2)
        self.pushButton_3.clicked.connect(self.pos_save_1)
        self.pushButton_4.clicked.connect(self.pos_save_2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def smoother(self):
        pass

    def servo_writer(self, servo_array):
        print(servo_array)
        pin6.write(servo_array[0])
        pin9.write(servo_array[1])
        pin10.write(servo_array[2])
        pin11.write(servo_array[3])

        '''
        adder_1 = 0
        adder_2 = 0
        adder_3 = 0
        adder_4 = 0

        i = 0
        for array in servo_array:
            if cur_value[i] > array:
                adder_1 = -1
            elif cur_value[i] < array:
                adder_1 = +1
            if cur_value[i] > array:
                adder_2 = -1
            elif cur_value[i] < array:
                adder_2 = +1
            if cur_value[i] > array:
                adder_3 = -1
            elif cur_value[i] < array:
                adder_3 = +1
            if cur_value[i] > array:
                adder_4 = -1
            elif cur_value[i] < array:
                adder_4 = +1
            i += 1

        while True:

            if servo_array[0] != cur_value[0]:
                pin6.write(cur_value[0]+adder_1)
                cur_value[0] += adder_1
            
            if servo_array[1] != cur_value[1]:
                pin9.write(cur_value[1]+adder_2)
                cur_value[1] += adder_2

            if servo_array[2] != cur_value[2]:
                pin10.write(cur_value[2]+adder_3)
                cur_value[2] += adder_3

            if servo_array[3] != cur_value[3]:
                pin11.write(cur_value[3]+adder_4)
                cur_value[3] += adder_4

            time.sleep(1)
            if servo_array[0] == cur_value[0] and servo_array[1] != cur_value[1] and servo_array[2] != cur_value[2] and servo_array[3] != cur_value[3]:
                pin6.write(cur_value[0])
                pin9.write(cur_value[1])
                pin10.write(cur_value[2])
                pin11.write(cur_value[3])
                break
        '''

    # Sliderlar hareket ettiği zaman bu fonksiyon çalışır.
    def pos(self):
        #if self.go_there:
        self.value1 = self.servo_1.sliderPosition()
        self.value2 = self.servo_2.sliderPosition()
        self.value3 = self.servo_3.sliderPosition()
        self.value4 = self.servo_4.sliderPosition()
        self.value_array = [self.value1,self.value2,self.value3,self.value4]
        self.servo_writer(self.value_array)

    def go_slider(self,slider_pos):
        self.servo_1.setValue(slider_pos[0])
        self.servo_2.setValue(slider_pos[0])
        self.servo_3.setValue(slider_pos[2])
        self.servo_4.setValue(slider_pos[3])

    # Save_1'e basıldıktan sonra bu fonksiyon çalışır.
    def pos_save_1(self):
        self.position_1 = [self.value1, self.value2, self.value3, self.value4]
        print(self.position_1)

    # Save_2'ye basıldıktan sonra bu fonksiyon çalışır.
    def pos_save_2(self):
        self.position_2 = [self.value1, self.value2, self.value3, self.value4]
        print(self.position_2)

    # 1'e basıldıktan sonra bu fonksiyon çalışır.
    def go_pos_1(self):
        #self.smoother()
        self.servo_writer(self.position_1)
        '''
        self.go_there = False
        self.go_slider(self.position_1)
        self.go_there = True
        '''
    
    # 2'ye basıldıktan sonra bu fonksiyon çalışır.
    def go_pos_2(self):
        #self.smoother()
        self.servo_writer(self.position_2)
        '''
        self.go_there = False
        self.go_slider(self.position_2)
        self.go_there = True
        '''
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "METU MECH"))
        self.pushButton.setText(_translate("MainWindow", "1"))
        self.pushButton_2.setText(_translate("MainWindow", "2"))
        self.pushButton_3.setText(_translate("MainWindow", "Save 1"))
        self.pushButton_4.setText(_translate("MainWindow", "Save 2"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
