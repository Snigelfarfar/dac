#!/usr/bin/python2.7
import sys
import time
from PyQt4.QtCore import QTime, QTimer, Qt
from PyQt4.QtGui import QMainWindow, QApplication, QLCDNumber, QPushButton, QPalette, QColor, QBrush

from src.dacui import Ui_DennysAlarmClock
from src.daclog import DacLog
from src.dacsettings import dacDefaultSettings
from src.dacfunc import DacFunc
import logging


DacLog()
log = logging.getLogger("dac-logger")
log.info("Initializing logging and starting Main application.")

class DennysAlarmClock(QMainWindow, Ui_DennysAlarmClock, DacFunc):
    def __init__(self, parent=None):
        super(DennysAlarmClock, self).__init__(parent)
        self.settings = dacDefaultSettings()
        self.setupUi(self)

       # self.PushButton2.clicked.connect(self.dacCloseApplication)
       # self.PushButton2.clicked.connect(self.OpenWindow2)
        self.btnInfo.clicked.connect(lambda: self.dacInfo(self.settings))
        self.btnPower.clicked.connect(self.dacCloseApplication) 
        self.btnSettings.clicked.connect(self.OpenWindow1)

        #Window2UI, options screen, return to main
        self.btnOptionReturn.clicked.connect(self.OpenWindow0)
        
        #Window3UI, Silence alarm screen
        #self.btn3SilenceAndReturn.clicked.connect(self.OpenWindow0)
        self.btn3SilenceAndReturn.clicked.connect(self.dacChallengeCheck)

        
        self.timeTracker = QTimer(self)
        self.timeTracker.start(60000)
        self.timeTracker.timeout.connect(self.dacEventTracker)

        log.info("INIT DONE")

    #Main Window, initial screen with time and settings etc
    def OpenWindow0(self):
        log.info("Openwindow0")
        #Triggered once we return to the main screen.
        self.stack0.showFullScreen()
        self.QtStack.setCurrentIndex(0)

    def OpenWindow1(self):
        #self.stack1.showFullScreen()
        self.QtStack.setCurrentIndex(1)

    def OpenWindow2(self):
        self.QtStack.setCurrentIndex(2)

def main():
    app = QApplication(sys.argv)
    clock = DennysAlarmClock()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

