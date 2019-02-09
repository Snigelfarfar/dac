from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtCore import QTimer, QTime, QSize
from PyQt4.QtGui import QWidget, QStackedLayout, QPushButton, QLCDNumber, QAction, QLineEdit, QTextEdit, QAbstractScrollArea

import os
import sys
import logging
import random
from pygame import mixer

from dacclasses import DacToolbarButton

log = logging.getLogger("dac-logger")

class Ui_DennysAlarmClock(QWidget):
    def setupUi(self, DennysAlarmClock):
        DennysAlarmClock.setObjectName("Main")
        DennysAlarmClock.resize(800, 480)

        self.QtStack = QStackedLayout()
        #self.QtStack.setStackingMode(0)

        self.stack0 = QWidget()
        self.stack1 = QWidget()
        self.stack2 = QWidget()

       # self.stack2.setStyleSheet("background: black")
        self.stack0.setStyleSheet("\
        QWidget{\
                background: gray;\
                color: #d1c6ff;\
        }\
        QLCDNumber{\
                border: 2px solid red;\
                border-radius: 4px;\
                border-color: #ebccff;\
                color: #ebccff;\
        }\
        ")
        self.stack2.setStyleSheet("\
        QWidget{\
                background: black;\
                font: bold 42px;\
                color: white;\
        }\
        QLineEdit{\
                border-style: solid;\
                border-width: 2px;\
                border-color: #ceafff;\
                border-radius: 25px;\
        }\
        QPushButton{\
                border-style: solid;\
                border-width: 2px;\
                border-color: #ceafff;\
                border-radius: 25px;\
               /* background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #c199ff, stop: 1 #8d46fc);\ */\
                }\
        QPushButton:pressed{\
                border-style: inset;\
                border-width: 2px;\
                border-color: #ceafff;\
                border-radius: 50px;\
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #c199ff, stop: 1 #8d46fc);\
                }\
        ")



        self.Window1UI()
        self.Window2UI()
        self.Window3UI()

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
       
        log.debug("setupUi(self, DennysAlarmClock)") 
        log.debug(self.settings)

    def Window1UI(self):
    #####################
    # MAIN ALARM WINDOW #
    #####################
        log.debug("Setting up Window1UI") #<__main__.DennysAlarmClock object at 0x74d87cb0>

        self.stack0.resize(800, 480)
        #print(self.stack0.windowState())

        #############
        # LCD FRAME #
        #############
        log.debug("Setting up LCD FRAME")
        #dacLcdFrame, draw first, under all other widgets
        self.lcdframe = self.dacLcdFrame()

        ##########
        # LABELS #
        ##########
        log.debug("Setting up LABELS")
        #Alarmtime
        self.lblAlarmTime = QtGui.QLabel(str(self.settings['time']['wakeup']), self.stack0)
        self.lblAlarmTime.move(15,60)

        #Bulb
        self.lblBulbTime = QtGui.QLabel(str(self.settings['time']['bulb']), self.stack0)
        self.lblBulbTime.move(115,60)

        #Coffee
        self.lblCoffeeTime = QtGui.QLabel("07:00", self.stack0)
        self.lblCoffeeTime.move(215,60)

        #self.alarmStatusIcon = QtGui.QAction(QtGui.QIcon("img/testicon.png"), 'test', self.stack0)

        #########
        # ICONS #
        #########
        log.debug("setting up ICONS")
        PWD_PATH = os.path.dirname(os.path.realpath(__file__))
        SVG_PATH = os.path.join(PWD_PATH, '../img/icons/svg')
        ICON_PATH = os.path.normpath(SVG_PATH)
        log.debug(ICON_PATH)
        #Add Icon
        self.testicon = QtGui.QIcon(os.path.join(ICON_PATH,"poweroff.svg"))
        self.iconCoffeeCup_off = QtGui.QIcon("img/icons/svg/cup.svg") 
        self.iconCoffeeCup_on = QtGui.QIcon("img/icons/svg/cup_hot.svg") 

        self.iconPower = QtGui.QIcon(os.path.join(ICON_PATH,"poweroff.svg"))

        #AlarmStatus
        #self.iconAlarmStatus_off  QtGui.QIcon(os.path.join(ICON_PATH,"alarmiconoff_filled.svg"))
        #self.iconAlarmStatus_off = QtGui.QIcon(os.path.join(ICON_PATH,"alarmiconoff.svg"))
        self.iconAlarmStatus_off = QtGui.QIcon(os.path.join(ICON_PATH,"alarmiconoffslashed.svg"))
        self.iconAlarmStatus_on = QtGui.QIcon(os.path.join(ICON_PATH,"alarmiconon.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"alarmiconon_filled.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"alarmiconslashed_filled.svg"))
        
        #Coffee related icons
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"beans_filled.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"beans.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"coffee_hot.svg"))
        self.iconCoffeeCup_hot =  QtGui.QIcon(os.path.join(ICON_PATH,"cup_hot.svg"))
        self.iconCoffeeCup = QtGui.QIcon(os.path.join(ICON_PATH,"cup.svg"))
        
        #BulbStatus
        self.iconBulbStatus_off =  QtGui.QIcon(os.path.join(ICON_PATH,"bulboff.svg"))
        self.iconBulbStatus_on =  QtGui.QIcon(os.path.join(ICON_PATH,"bulb.svg"))
        
        #Calendar icons
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"calendarday_filled.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"calendarday.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"calendaricon_filled.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"calendaricon.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"calendaroff_filled.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"calendaroff.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"calendaron_filled.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"calendaron.svg"))

        #Clock icons
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"clock_filled.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"clock.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"timearrow_filled.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"timearrow.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"24hoursfree_filled.svg")
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"24hoursfree.svg")

        #Weather related icons
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"cloud.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"mountains_filled.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"mountains.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"raining_filled.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"raining.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"rain.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"snow_filled.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"snowflake_color.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"snowflake_filled.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"snowflake.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"snowing.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"thermometer_cold_color.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"thermometer_cold_filled.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"thermometer_cold.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"thermometer_hot_filled.svg

        #Hourglass icons
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"hourglassempty_filled.svg"))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"hourglassempty.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"hourglassfull_filled.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"hourglassfull.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"hourglassicon_fileld.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"hourglassicon.svg

        #Lock icons
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"lock_closed_filled.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"lock_closed.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"lock_open_filled.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"lock_open.svg

        #Settings icons
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"settings_cog_detailed_filled.svg
        self.iconSettings =  QtGui.QIcon(os.path.join(ICON_PATH,'settings_cog_detailed.svg'))
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"settings_cog_filled.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"settings_cog.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"youtube_filled.svg
        #self.icon =  QtGui.QIcon(os.path.join(ICON_PATH,"youtube.svg

        ###########
        # BUTTONS #
        ###########
        log.debug("setting up BUTTONS")

        self.testbutton = QPushButton(self.stack0)
        self.testbutton.setGeometry(340,30,60,60)
        self.testbutton.setIconSize(QSize(60,60))


        #Alarm status button
        self.btnAlarmStatus = QPushButton(self.stack0)
        self.btnAlarmStatus.setFlat(True)
        self.btnAlarmStatus.setGeometry(10,10,50,50)
        self.btnAlarmStatus.setIconSize(QSize(50,50))
        self.btnAlarmStatus.setStyleSheet("QPushButton{border: 0px solid;}")
       #self.btnAlarmStatus.clicked.connect(self.dacToggleAlarmStatus)
        self.btnAlarmStatus.setCheckable(True)
        self.btnAlarmStatus.toggled.connect(self.dacToggleAlarmStatus)
        
        if self.settings['status']['wakeup'] == 'OFF':
            self.btnAlarmStatus.setIcon(self.iconAlarmStatus_off)
        else:
            self.btnAlarmStatus.setIcon(self.iconAlarmStatus_on)
            self.btnAlarmStatus.setChecked(True)

        #Bulb status button
        self.btnBulbStatus = QPushButton(self.stack0)
        self.btnBulbStatus.setFlat(True)
        #TODO: at initial startup, check status of bulb and set the appropriate icon.
        self.btnBulbStatus.setIcon(self.iconBulbStatus_off)
        self.btnBulbStatus.setGeometry(110,10,50,50)
        self.btnBulbStatus.setIconSize(QSize(50,50))
        self.btnBulbStatus.setStyleSheet("QPushButton{border: 0px solid;}")
       #self.btnBulbStatus.clicked.connect(self.dacToggleBulbStatus)
        self.btnBulbStatus.setCheckable(True)
        self.btnBulbStatus.toggled.connect(self.dacToggleBulbStatus)

        #CoffeeCup status button
        self.btnCoffeeCupStatus = QPushButton(self.stack0)
        self.btnCoffeeCupStatus.setFlat(True)
        self.btnCoffeeCupStatus.setIcon(self.iconCoffeeCup)
        self.btnCoffeeCupStatus.setGeometry(210,10,50,50)
        self.btnCoffeeCupStatus.setIconSize(QSize(50,50))
        self.btnCoffeeCupStatus.setStyleSheet("QPushButton{border: 0px solid;}")
        self.btnCoffeeCupStatus.setCheckable(True)
        self.btnCoffeeCupStatus.toggled.connect(self.dacToggleCoffeeCupStatus)

        #Info button
        self.btnInfo = QPushButton(self.stack0)
        self.btnInfo.setFlat(True)
        self.btnInfo.setIcon(self.iconSettings)
        self.btnInfo.setGeometry(540,10,50,50)
        self.btnInfo.setIconSize(QSize(50,50))
        self.btnInfo.setStyleSheet("QPushButton{border: 0px solid;}")
        #self.btnSettingsStatus.clicked.connect(self.dacToggleSettingsStatus)
        #self.btnSettingsStatus.setCheckable(True)
        #self.btnSettingsStatus.toggled.connect(self.dacToggleSettingsStatus)

        #Settings status button
        self.btnSettings = QPushButton(self.stack0)
        self.btnSettings.setFlat(True)
        self.btnSettings.setIcon(self.iconSettings)
        self.btnSettings.setGeometry(740,10,50,50)
        self.btnSettings.setIconSize(QSize(50,50))
        self.btnSettings.setStyleSheet("QPushButton{border: 0px solid;}")
        #self.btnSettingsStatus.clicked.connect(self.dacToggleSettingsStatus)
        #self.btnSettingsStatus.setCheckable(True)
        #self.btnSettingsStatus.toggled.connect(self.dacToggleSettingsStatus)

        #Power status button
        self.btnPower = QPushButton(self.stack0)
        self.btnPower.setFlat(True)
        self.btnPower.setIcon(self.iconPower)
        self.btnPower.setShortcut("q")
        self.btnPower.setGeometry(640,10,50,50)
        self.btnPower.setIconSize(QSize(50,50))
        self.btnPower.setStyleSheet("QPushButton{border: 0px solid;}")

        #PushButton1
        # Hidden silence button, deactivated unless the alarm is running
        self.btn1SilenceAlarm = QPushButton(self.stack0)
        self.btn1SilenceAlarm.setText("SILENCE")
        self.btn1SilenceAlarm.setFlat(True)
        self.btn1SilenceAlarm.setGeometry(QtCore.QRect(0, 100, 800, 280))
        self.btn1SilenceAlarm.setEnabled(False)
        #Window1UI, main alarm window
        self.btn1SilenceAlarm.clicked.connect(self.OpenWindow2)

        #Log frame
        self.txtLogInput = QTextEdit(self.stack0)
        self.txtLogInput.setGeometry(5,375,790,100)
        self.txtLogInput.setStyleSheet("QTextEdit{border: 1px solid;border-color: black;}")
        self.txtLogInput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtLogInput.setReadOnly(True)
        self.txtLogInput.append("Hello, this is logging")

       # #PushButton2# just close for now
       # self.PushButton2 = QPushButton(self.stack0)
       # #self.PushButton2.setText("Quit")
       # self.PushButton2.setShortcut("q")
       # self.PushButton2.setGeometry(QtCore.QRect(10, 230, 60, 50))
       # self.PushButton2.setIcon(self.testicon)
       # self.PushButton2.setStyleSheet("QPushButton{border: 0px solid;}")
       # #this shows a lcd frame,
       # #self.lcdframe = QLCDNumber(self.stack0) 

        #Finally, set first stack to fullscreen.
        #Only applies the first time we open the application
        self.stack0.showFullScreen()

    def Window2UI(self):
    ##################
    # OPTIONS WINDOW #
    ##################
        log.debug("Setting up Window2UI")
        self.stack1.resize(800, 480)
        self.btnOptionReturn = QPushButton(self.stack1)
        self.btnOptionReturn.setText("Return")
        self.btnOptionReturn.setGeometry(QtCore.QRect(600, 380, 100, 100))
        #self.stack1.setStyleSheet("background: red")

        self.btnOptionSave = QPushButton(self.stack1)
        self.btnOptionSave.setText("Save")
        self.btnOptionSave.setGeometry(QtCore.QRect(700, 380, 100, 100))

        self.btnOptionDebug = QPushButton(self.stack1)
        self.btnOptionDebug.setGeometry(QtCore.QRect(700, 10, 50, 50))

        self.btnOption2 = QPushButton(self.stack1)
        self.btnOption2.setGeometry(QtCore.QRect(700, 70, 50, 50))

        self.btnOption3 = QPushButton(self.stack1)
        self.btnOption3.setGeometry(QtCore.QRect(700, 130, 50, 50))

        self.btnOption4 = QPushButton(self.stack1)
        self.btnOption4.setGeometry(QtCore.QRect(700, 190, 50, 50))

        self.btnOption5 = QPushButton(self.stack1)
        self.btnOption5.setGeometry(QtCore.QRect(700, 250, 50, 50))

        self.btnOption6 = QPushButton(self.stack1)
        self.btnOption6.setGeometry(QtCore.QRect(700, 310, 50, 50))

    def Window3UI(self):
    #######################
    # UNLOCK ALARM WINDOW #
    #######################
        self.stack2.resize(800, 480)
        #self.stack2.setStyleSheet("background: blue")

        #Challenge text response
        self.txtChallengeInput = QLineEdit(self.stack2)
        self.txtChallengeInput.setGeometry(5,3,320,155)
        
        #Challenge text
        self.txtChallenge = QLineEdit(self.stack2)
        self.txtChallenge.setGeometry(5,161,320,155)
        self.dacGenerateChallenge()    
        self.txtChallenge.setText(self.settings['silence']['challenge'])    

        #Silence button
        self.btn3SilenceAndReturn = QPushButton(self.stack2)
        self.btn3SilenceAndReturn.setText("SILENCE!!!")
        self.btn3SilenceAndReturn.setGeometry(QtCore.QRect(5,319,320,155))
        
        #300, 350, 400
        self.btn3NumPad1 = QPushButton(self.stack2)
        self.btn3NumPad1.setText("1")
        self.btn3NumPad1.setGeometry(QtCore.QRect(335,3,155,155))
        self.btn3NumPad1.clicked.connect(self.dacNumPadSetText)

        self.btn3NumPad2 = QPushButton(self.stack2)
        self.btn3NumPad2.setText("2")
        self.btn3NumPad2.setGeometry(QtCore.QRect(490,3,155,155))
        self.btn3NumPad2.clicked.connect(self.dacNumPadSetText)

        self.btn3NumPad3 = QPushButton(self.stack2)
        self.btn3NumPad3.setText("3")
        self.btn3NumPad3.setGeometry(QtCore.QRect(645,3,155,155))
        self.btn3NumPad3.clicked.connect(self.dacNumPadSetText)

        self.btn3NumPad4 = QPushButton(self.stack2)
        self.btn3NumPad4.setText("4")
        self.btn3NumPad4.setGeometry(QtCore.QRect(335,161,155,155))
        self.btn3NumPad4.clicked.connect(self.dacNumPadSetText)

        self.btn3NumPad5 = QPushButton(self.stack2)
        self.btn3NumPad5.setText("5")
        self.btn3NumPad5.setGeometry(QtCore.QRect(490,161,155,155))
        self.btn3NumPad5.clicked.connect(self.dacNumPadSetText)

        self.btn3NumPad6 = QPushButton(self.stack2)
        self.btn3NumPad6.setText("6")
        self.btn3NumPad6.setGeometry(QtCore.QRect(645,161,155,155))
        self.btn3NumPad6.clicked.connect(self.dacNumPadSetText)
        
        self.btn3NumPad7 = QPushButton(self.stack2)
        self.btn3NumPad7.setText("7")
        self.btn3NumPad7.setGeometry(QtCore.QRect(335,319,155,155))
        self.btn3NumPad7.clicked.connect(self.dacNumPadSetText)

        self.btn3NumPad8 = QPushButton(self.stack2)
        self.btn3NumPad8.setText("8")
        self.btn3NumPad8.setGeometry(QtCore.QRect(490,319,155,155))
        self.btn3NumPad8.clicked.connect(self.dacNumPadSetText)

        self.btn3NumPad9 = QPushButton(self.stack2)
        self.btn3NumPad9.setText("9")
        self.btn3NumPad9.setGeometry(QtCore.QRect(645,319,155,155))
        self.btn3NumPad9.clicked.connect(self.dacNumPadSetText)


