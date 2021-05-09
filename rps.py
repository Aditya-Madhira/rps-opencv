

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QLabel
import cv2
from PyQt5.QtGui import QPixmap, QColor,QImage
from PyQt5.QtCore import QThread,Qt,pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from tensorflow.keras.models import load_model
import numpy as np
import random
import pyrebase
import os
import h5py

firebaseConfig = {
    'apiKey': "AIzaSyC12aYZt7hSfODLevEiUY0qeCAffUn7exc",
    'authDomain': "rpscv-112ee.firebaseapp.com",
    'projectId': "rpscv-112ee",
    'storageBucket': "rpscv-112ee.appspot.com",
    "databaseURL" : "",
    'messagingSenderId': "471623644637",
    'appId': "1:471623644637:web:c2870666f91d9fed1cb234"
  }
firebase = pyrebase.initialize_app(firebaseConfig)
mystorage = firebase.storage()













class twindow():
    def __init__(self):
            self.tmain = QtWidgets.QMainWindow()
            self.tmain.resize(500, 380)
            self.wid = QtWidgets.QWidget(self.tmain)
            self.wid.resize(500, 380)
            self.lab = QtWidgets.QLabel(self.wid)
            self.lab.setText("press x on cv2 window to start")
            self.lab.resize(300,200)
            self.wid.show()
            self.tmain.show()
    def updatelab(self,uans,cans,res):
        self.lab.setText("Your move is :{x} VS computer move is :{y}\nThe result is:{z}".format(x=uans,y=cans,z=res))
        self.lab.adjustSize()









class Ui_MainWIn(object):
    path="None"



    def setupUi(self, MainWIn):


        MainWIn.setObjectName("MainWIn")
        MainWIn.resize(1122, 694)

        self.centralwidget = QtWidgets.QWidget(MainWIn)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.resize(1122, 694)

        self.Headlabel = QtWidgets.QLabel(self.centralwidget)
        self.Headlabel.setGeometry(QtCore.QRect(510, 10, 71, 21))
        self.Headlabel.setSizeIncrement(QtCore.QSize(30, 30))
        self.Headlabel.setObjectName("Headlabel")

        self.radioButton1 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton1.setGeometry(QtCore.QRect(20, 500, 95, 20))
        self.radioButton1.setObjectName("radioButton1")

        self.radioButton2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton2.setGeometry(QtCore.QRect(180, 500, 95, 20))
        self.radioButton2.setObjectName("radioButton2")

        self.question = QtWidgets.QLabel(self.centralwidget)
        self.question.setGeometry(QtCore.QRect(20, 430, 321, 16))
        self.question.setObjectName("question")

        self.pathbu = QtWidgets.QPushButton(self.centralwidget)
        self.pathbu.setGeometry(QtCore.QRect(790, 460, 211, 51))
        self.pathbu.setObjectName("pushButton")
        self.pathbu.clicked.connect(lambda param:self.setpath(self.centralwidget))








        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 100, 1111, 161))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(450, 540, 211, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda param1:self.open_cv(MainWIn))
        MainWIn.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWIn)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1122, 26))
        self.menubar.setObjectName("menubar")
        MainWIn.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWIn)
        self.statusbar.setObjectName("statusbar")
        MainWIn.setStatusBar(self.statusbar)

        self.retranslateUi(MainWIn)
        QtCore.QMetaObject.connectSlotsByName(MainWIn)

    def setpath(self,centralwid):
        text,ok=QInputDialog.getText(centralwid,"path set","Enter Path")
        if ok:
            self.path=text
            msg=QMessageBox()
            msg.setText("wait 10 seconds for the model to download")
            x=msg.exec_()
            mystorage.child("rps_rgb.h5").download(self.path+'/'+'model.h5')
            newmsg=QMessageBox()
            newmsg.setText("Done,click lets go")
            y=newmsg.exec_()
        if not ok:
            pass


    def open_cv(self,mainwinobj):
        print(self.path)




        mainwinobj.close()
        tobj = twindow()

        self.mymod = load_model(self.path+'/'+'model.h5')
        print("reached")

        self.label_names = ['Paper', 'Rock', 'Scissors', 'Nothing']

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            nocampop = QMessageBox()
            nocampop.setText("Webcam not found or not open(check settings)")
            x = nocampop.exec_()
            sys.exit()


        while True:

            self.ret, self.frame = self.cap.read()

            if not self.ret:
                nocampop=QMessageBox()
                nocampop.setText("Unable to read from webcam")
                x=nocampop.exec_()
                break
            self.frame = cv2.resize(self.frame, (852, 520))

            self.frame = cv2.flip(self.frame, 1)

            self.dis = cv2.rectangle(self.frame.copy(), (540, 10), (852, 320), (255, 0, 255), 2)
            self.roi = self.dis[10:320, 540:852]
            self.roi = np.expand_dims(self.roi, axis=0)
            self.pred = self.mymod.predict(self.roi)
            # Get the index of the target class.

            self.target_index = np.argmax(self.pred[0])

            self.prob = np.max(self.pred[0])

            cv2.putText(self.dis,
                        "prediction: {} {:.2f}%".format(self.label_names[int(self.target_index)], self.prob * 100),
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.90, (0, 0, 255), 2, cv2.LINE_AA)

            # Get model'

            cv2.imshow("Rock Paper Scissors", self.dis)

            k = cv2.waitKey(1)

            if k == ord('q'):
                break
            elif k == ord('x'):
                self.game(self.label_names[int(self.target_index)], tobj)
        self.cap.release()

        cv2.destroyAllWindows()

    def game(self,userans,tobj):
        guessl=["rock","Paper","Scissors"]

        

        compans=random.choice(guessl)
        res=""
        if userans=="Rock":
            if compans=="Rock":
                res="draw"
            elif compans=="Scissors":
                res="win"
            elif compans=="Paper":
                res="lost"
        if userans=="Paper":
            if compans=="Rock":
                res="win"
            elif compans=="Scissors":
                res="lost"
            elif compans=="Paper":
                res="draw"
        if userans=="Scissors":
            if compans=="Rock":
                res="lost"
            elif compans=="Scissors":
                res="draw"
            elif compans=="Paper":
                res="win"
        tobj.updatelab(userans,compans,res)

        




    def retranslateUi(self, MainWIn):
        _translate = QtCore.QCoreApplication.translate
        MainWIn.setWindowTitle(_translate("MainWin", "RPS_test"))
        self.Headlabel.setText(_translate("MainWin", "RPS Test"))
        self.radioButton1.setText(_translate("MainWin", "Yes"))
        self.radioButton2.setText(_translate("MainWin", "No"))
        self.pathbu.setText(_translate("MainWin", "Set Path"))
        self.question.setText(_translate("MainWin", "Do you have the model in your system?"))

        self.textBrowser.setHtml(_translate("MainWin", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Instructions</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">1)Click next to test the game.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">2)Webcam is needed.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">3)Make sure webcam is facing you.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">4)current version only works if the background is white.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">HOW TO PLAY:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">1) There will be a purple box which will be displayed to you</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">2) Select an option from the checkbox</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">3)make sure your hand is in the box area.THE BACKGROUND MUST BE A WHITE WALL.</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWin", "Lets Go"))










if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWIn = QtWidgets.QMainWindow()
    ui = Ui_MainWIn()
    ui.setupUi(MainWIn)
    MainWIn.show()
    sys.exit(app.exec_())
