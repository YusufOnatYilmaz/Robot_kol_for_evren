#!/usr/bin/env python3
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pyfirmata

board = pyfirmata.Arduino("COM3")
iter8 = pyfirmata.util.Iterator(board)
iter8.start()
pin6 = board.get_pin('d:6:s')
pin9 = board.get_pin('d:9:s')
pin10 = board.get_pin('d:10:s')
pin11 = board.get_pin('d:11:s')
pin_array = [pin6,pin9,pin10,pin11]

class Ui_MainWindow(object):

    def initiator(self):
        self.value1 = 0
        self.value2 = 0
        self.value3 = 0
        self.value4 = 0
        self.position_1 = [90,90,90,90]
        self.position_2 = [90,90,90,90]
        self.go_there = True

        #sliderların sınırlarını 100'den 180'e alma
        self.servo_1.setMaximum(180)
        self.servo_2.setMaximum(180)
        self.servo_3.setMaximum(180)
        self.servo_4.setMaximum(180)
        self.servo_1.setValue(self.value1)
        self.servo_2.setValue(self.value2)
        self.servo_3.setValue(self.value3)
        self.servo_4.setValue(self.value4)
        pin_array[0].write(self.value1)
        pin_array[1].write(self.value2)
        pin_array[2].write(self.value3)
        pin_array[3].write(self.value4)

        #sliderlerin değerleri değiştiği zaman pos fonksiyonu çalışır.
        self.servo_1.valueChanged.connect(self.pos)  
        self.servo_2.valueChanged.connect(self.pos)
        self.servo_3.valueChanged.connect(self.pos)
        self.servo_4.valueChanged.connect(self.pos)

        # butonları ilgili fonksiyonlara atama
        self.go_button_1.clicked.connect(self.go_pos_1)
        self.go_button_2.clicked.connect(self.go_pos_2)
        self.save_button_1.clicked.connect(self.pos_save_1)
        self.save_button_2.clicked.connect(self.pos_save_2)
        self.for_button.clicked.connect(self.forward_kinematics)
        self.inv_button.clicked.connect(self.inverse_kinematics)
        self.stabilizer_button.clicked.connect(self.stabilizer)
 
    def inverse_kinematics(self):
        pass

    def forward_kinematics(self):
        pass

    def stabilizer(self):
        self.smoother(saved_pos=[0,0,0,0],current_pos=[0,180,180,0])

    # Motorları açı değerlerini smoothing işlemine sokuyoruz sonra o pozisyona götürüyoruz.
    def smoother(self, saved_pos, current_pos):

        smoothing_factor = []
        for i in range(len(saved_pos)):
            smoothing_factor.append(abs(saved_pos[i] - current_pos[i])/100)

        saved_pos_factor = 0.03
        
        while True:

            for i in range(len(saved_pos)):
                if abs(saved_pos[i] - current_pos[i]) >   smoothing_factor[i]:
                    # smoothing işlemi
                    servo_smoothed = saved_pos[i]*saved_pos_factor + current_pos[i]*(1-saved_pos_factor)
                    pin_array[i].write(servo_smoothed)
                    current_pos[i] = servo_smoothed
            
            board.pass_time(0.02)
            print(saved_pos, current_pos)
            if (abs(saved_pos[0] - current_pos[0]) <= smoothing_factor[0]) and (abs(saved_pos[1] - current_pos[1]) <= smoothing_factor[1]) and (abs(saved_pos[2] - current_pos[2]) <= smoothing_factor[2]) and (abs(saved_pos[3] - current_pos[3]) <= smoothing_factor[3]):
                self.go_slider(current_pos)
                break

    # Sliderlar hareket ettiği zaman bu fonksiyon çalışır.
    def pos(self):
        if self.go_there:
            # Sliderların pozisyonunu anlık pozisyonunu alıp motorları çalıştırıyoruz.
            self.value1 = self.servo_1.sliderPosition()
            self.value2 = self.servo_2.sliderPosition()
            self.value3 = self.servo_3.sliderPosition()
            self.value4 = self.servo_4.sliderPosition()
            pin6.write(self.value1)
            pin9.write(self.value2)
            pin10.write(self.value3)
            pin11.write(self.value4)
            self.value_array = [self.value1,self.value2,self.value3,self.value4]


    def go_slider(self, slider_pos):
        self.servo_1.setValue(int(slider_pos[0]))
        self.servo_2.setValue(int(slider_pos[1]))
        self.servo_3.setValue(int(slider_pos[2]))
        self.servo_4.setValue(int(slider_pos[3]))


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
        self.smoother(self.position_1,self.value_array)
        # motorları götürdükten sonra bir de sliderları yeni pozisyona götürüyoruz
        self.go_there = False
        self.go_slider(self.position_1)
        self.go_there = True


    # 2'ye basıldıktan sonra bu fonksiyon çalışır.
    def go_pos_2(self):
        self.smoother(self.position_2,self.value_array)
        self.go_there = False
        self.go_slider(self.position_2)
        self.go_there = True


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(906, 559)
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
        self.go_button_1 = QtWidgets.QPushButton(self.centralwidget)
        self.go_button_1.setGeometry(QtCore.QRect(170, 400, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.go_button_1.setFont(font)
        self.go_button_1.setObjectName("go_button_1")
        self.go_button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.go_button_2.setGeometry(QtCore.QRect(320, 400, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.go_button_2.setFont(font)
        self.go_button_2.setObjectName("go_button_2")
        self.save_button_1 = QtWidgets.QPushButton(self.centralwidget)
        self.save_button_1.setGeometry(QtCore.QRect(170, 450, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.save_button_1.setFont(font)
        self.save_button_1.setObjectName("save_button_1")
        self.save_button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.save_button_2.setGeometry(QtCore.QRect(320, 450, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.save_button_2.setFont(font)
        self.save_button_2.setObjectName("save_button_2")
        self.stabilizer_button = QtWidgets.QPushButton(self.centralwidget)
        self.stabilizer_button.setGeometry(QtCore.QRect(580, 100, 91, 51))
        self.stabilizer_button.setObjectName("stabilizer_button")
        self.empty_area_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.empty_area_1.setGeometry(QtCore.QRect(580, 210, 201, 31))
        self.empty_area_1.setText("")
        self.empty_area_1.setObjectName("empty_area_1")
        self.empty_area_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.empty_area_2.setGeometry(QtCore.QRect(580, 290, 201, 31))
        self.empty_area_2.setObjectName("empty_area_2")
        self.forward_kinematics_text = QtWidgets.QLabel(self.centralwidget)
        self.forward_kinematics_text.setGeometry(QtCore.QRect(580, 180, 221, 17))
        self.forward_kinematics_text.setObjectName("forward_kinematics_text")
        self.inverse_kinematics_text = QtWidgets.QLabel(self.centralwidget)
        self.inverse_kinematics_text.setGeometry(QtCore.QRect(580, 260, 221, 17))
        self.inverse_kinematics_text.setObjectName("inverse_kinematics_text")
        self.for_button = QtWidgets.QPushButton(self.centralwidget)
        self.for_button.setGeometry(QtCore.QRect(800, 210, 51, 31))
        self.for_button.setText("")
        self.for_button.setObjectName("for_button")
        self.inv_button = QtWidgets.QPushButton(self.centralwidget)
        self.inv_button.setGeometry(QtCore.QRect(800, 290, 51, 31))
        self.inv_button.setText("")
        self.inv_button.setObjectName("inv_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 906, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.initiator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "METU MECH"))
        self.go_button_1.setText(_translate("MainWindow", "1"))
        self.go_button_2.setText(_translate("MainWindow", "2"))
        self.save_button_1.setText(_translate("MainWindow", "Save 1"))
        self.save_button_2.setText(_translate("MainWindow", "Save 2"))
        self.stabilizer_button.setText(_translate("MainWindow", "Stabilizer"))
        self.forward_kinematics_text.setText(_translate("MainWindow", "Forward Kinematics"))
        self.inverse_kinematics_text.setText(_translate("MainWindow", "Inverse Kinematics"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
