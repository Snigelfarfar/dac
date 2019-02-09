import logging, sys, os
from logging import config
from PyQt4.QtGui import QTextEdit, QLineEdit, QPushButton
from PyQt4.QtCore import QSize

class DacHandler(logging.Handler):
    #parent fuckery
    def __init__(self,parent):
        logging.StreamHandler.__init__(self)
        #super().__init__()
        self.widget = QTextEdit(parent)

    def emit(self, record):
        msg = self.format(record)
        self.widget.append(msg)
        #DennysAlarmClock.txtLogInput.append("Men huur")

class DacToolbarButton(QPushButton):
    def __init__(self):
        super(DacToolbarButton,self).__init__()
        self.setFlat(False)
       # self.setIcon(self.iconPower)
        self.setGeometry(340,30,60,60)
        self.setIconSize(QSize(60,60))
        #self.setStyleSheet("QPushButton{border: 0px solid;}")
