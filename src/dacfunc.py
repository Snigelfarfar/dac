from PyQt4 import QtCore, QtGui, Qt
from PyQt4.QtCore import QTimer, QTime, QSize
from PyQt4.QtGui import QWidget, QStackedLayout, QPushButton, QLCDNumber, QAction, QLineEdit, QTextEdit, QAbstractScrollArea

import os
import sys
import logging
import random
from pygame import mixer
from api.homeassistant import lightswitch

log = logging.getLogger("dac-logger")

class DacFunc():

    def dacToggleAlarmStatus(self, checked):
        if checked:
            self.btnAlarmStatus.setIcon(self.iconAlarmStatus_on)
            self.lblAlarmTime.setVisible(True)
            self.settings['status']['wakeup'] = 'ON'
            log.debug("checked")
        else:
            self.btnAlarmStatus.setIcon(self.iconAlarmStatus_off)
            self.lblAlarmTime.setVisible(False)
            self.settings['status']['wakeup'] = 'OFF'
            log.debug("unchecked")

        log.debug("btnStatusButton enabled: {}".format(self.btnAlarmStatus.isEnabled()))

        self.btnAlarmStatus.setEnabled(True)

    def dacLcdFrame(self):
        log.debug("Setting up lcdFrame")
        lcdFrame = QLCDNumber(self.stack0)
        lcdFrame.resize(800, 480)
        #lcdFrame.resize(400, 240)
        lcdFrame.setSegmentStyle(QLCDNumber.Filled)

        timer = QTimer(self)
        timer.timeout.connect(lambda: self.showTime(lcdFrame))
        timer.start(1000)
        
    def showTime(self, led):
        time = QTime.currentTime()
        text = time.toString('hh:mm')

        current_alarm = self.settings['time']['wakeup']
        current_teamflash = self.settings['time']['bulb']
        
        time_to_turn_off_bulb = "23:42" 

        time_to_str = str("%s" % text)
        
        #print("text {}".format(text))
        #self.PushButton2.setVisible(True)

        #if (time.second() % 2) == 0:
        #    text = text[:2] + ' ' + text[3:]

        led.display(text)
    
    def dacEventTracker(self):
        log.debug("EVENT TRACKER CHECKING IN!")

        time = QTime.currentTime()
        text = time.toString('hh:mm')

        current_alarm = self.settings['time']['wakeup']
        current_teamflash = self.settings['time']['bulb']
        
        time_to_turn_off_bulb = self.dacAddToTime(current_teamflash, self.settings['timer']['bulb']) 

        log.debug("time_to_turn_off_bulb: {}".format(time_to_turn_off_bulb))

        time_to_str = str("%s" % text)

        #Check this again, its probably garbage
        if self.settings['status']['wakeup'] == 'ON':
            # if time to wake up
            if time_to_str in current_alarm:
                self.dacSoundTheAlarm()
            if time_to_str > current_alarm and self.settings['trigger']['wakeup'] == 'OFF':
                self.settings['trigger']['wakeup'] = 'ON'
                log.debug("Alarm time has passed, resetting alarm trigger")
        
        if self.settings['status']['bulb'] == 'ON':
            log.debug("?")
            if time_to_str in current_teamflash:
                log.debug("status.bulb = on, and time is now. Prepare for teamflash.")
                self.dacTeamFlash(True)
                try:
                    QTimer.singleShot(1800000, lambda: self.dacTeamFlash(False))
                except Exception as e:
                    log.debug(e)

        #QTimer.singleShot(10000, self.dacInfo)

    def dacToggleBulbStatus(self, checked):
        bulb_id = self.settings['api']['homeassistant']['bulb']['id']
        if checked:
            log.debug("Bulb switched ON")
            self.btnBulbStatus.setIcon(self.iconBulbStatus_on)
            # TURN ON LIGHTS
            lightswitch.switch(bulb_id, 'turn_on', 1) 
            bulb_state = lightswitch.get_states(bulb_id) 
            log.debug(bulb_state)
            
        else:
            log.debug("Bulb switched OFF")
            self.btnBulbStatus.setIcon(self.iconBulbStatus_off)
            # TURN OFF LIGHTS
            lightswitch.switch(bulb_id, 'turn_off', 1) 
            bulb_state = lightswitch.get_states(bulb_id) 
            log.debug(bulb_state)

    def dacToggleCoffeeCupStatus(self, checked):
        if checked:
            self.btnCoffeeCupStatus.setIcon(self.iconCoffeeCup_hot)
            log.debug("checked")
            try:
                self.dacPlaySoundFile("kaka", True)
            except Exception as e:
                log.error("unable to call self.dacPlaySoundFile() due to reason: {}".format(e))
        else:
            self.btnCoffeeCupStatus.setIcon(self.iconCoffeeCup)
            try:
                self.dacPlaySoundFile("kaka", False)
            except Exception as e:
                log.error("unable to call self.dacPlaySoundFile() due to reason: {}".format(e))
            log.debug("not checked")

    def dacSoundTheAlarm(self):
        if self.settings['trigger']['wakeup'] == 'ON':
            #Enable silence button
            self.btn1SilenceAlarm.setEnabled(True)
            #Make noise
            self.dacPlaySoundFile("kaka", True)
            log.debug("ALARRRMA!!!!")
            #Dont trigger alarm again
            self.settings['trigger']['wakeup'] = 'OFF'

    def dacNumPadSetText(self):
        button = self.sender()
        value = str(button.text())

        log.debug("Pressed numpad button: {}".format(value))
         
        if self.settings['silence']['response'] == 'empty':
            self.settings['silence']['response'] = value
            self.txtChallengeInput.setText(self.settings['silence']['response'])
        else:
            if len(self.settings['silence']['response']) < 5:
                self.settings['silence']['response'] += value
        
                self.txtChallengeInput.setText(self.settings['silence']['response'])

    def dacChallengeCheck(self):
        log.debug("CHECKING challenge: {}, response: {}".format(self.settings['silence']['challenge'], self.settings['silence']['response']))
        
        #TODO: FIX THIS SHIT, WE ARE INPUTTING SOMEWHERE FUCKED
        if str("%s" % self.settings['silence']['challenge']) == str("%s" % self.settings['silence']['response']):
            #SUCCESS
            log.debug("SUCCESS challenge: {}, response: {}".format(self.settings['silence']['challenge'], self.settings['silence']['response']))
            
            #TODO:
            # - silence alarm
            # - reset response
            # - plaket
            
            #back to main alarm screen
            self.QtStack.setCurrentIndex(0)
            self.stack0.showFullScreen()

            self.txtChallengeInput.setText("YATTA")
            self.settings['silence']['completed'] = True
            log.debug("Setting silece:completed to: {}".format(self.settings['silence']['completed']))
            log.debug("Silencing alarm")
            self.dacPlaySoundFile("kaka", False)
            self.btn1SilenceAlarm.setEnabled(False)
        else:
            log.debug("FAIL challenge: {} {}, response: {} {}".format(type(self.settings['silence']['challenge']), self.settings['silence']['challenge'], type(self.settings['silence']['response']), self.settings['silence']['response']))
            self.settings['silence']['response'] = ''
            self.txtChallengeInput.setText(self.settings['silence']['response'])

        self.dacGenerateChallenge()


            #FAIL
    def dacGenerateChallenge(self):
        try:
            challenge = '0'
            #challenge = str(int(self.settings['silence']['challenge']) + 1)
            #challenge = str(self.dacGenerateRandomNumber())[:5]
            found_challenge = False
            while  not (found_challenge):
                if '0' in challenge:
                    log.debug("0 found in challenge, generating..")
                    challenge = str(self.dacGenerateRandomNumber())[:5]
                else:
                    log.debug("finally found a worthy challenge: {}".format(challenge))
                    found_challenge = True

            log.debug("Setting challenge: {}".format(challenge))
            
            #Update challenge
            self.settings['silence']['challenge'] = challenge
            self.txtChallenge.setText(str(challenge))
        except Exception as e:
            log.debug("Failed with reason: {}".format(e))
    
    def dacGenerateRandomNumber(self):
        randomint = random.randint(555556,666667)
        log.debug("Generated: {}".format(randomint))
        return randomint
    
    def dacAddToTime(self, time, minutes):
        log.debug("time {}".format(time))
        log.debug("minutes: {}".format(minutes))

        #minutes = int(timeframe) % 60
        
        pre_hour = time[:2]
        pre_minute = time[3:]
        
        total_minutes = int(pre_minute) + int(minutes)

        hours_to_add = int(total_minutes) / 60

        new_hour = int(pre_hour) + int(hours_to_add)
        new_minutes = int(total_minutes) % 60
        
        #fixme: time is not returned as 08:00 but 8:00 for example.

        new_time = str(new_hour) + ':' + str(new_minutes)
        log.debug(new_time)
        return new_time


    def dacPlaySoundFile(self, soundfile, play):
        #player = subprocess.Popen(["mplayer", "bacon-alarm.mp3", ]) 
        if play:
            log.debug("Playing sound: {}".format(soundfile))
            try:
                mixer.init()
                mixer.music.load("/home/pi/Projects/Alarmclock/sound/alarma-efecto-de-sonido.mp3")
                mixer.music.play(-1)
            except Exception as e:
                log.debug("Unable to play sound due to reason: {}".format(e))
        else:
            mixer.music.stop()
    
    
    def dacTeamFlash(self, activate):
        bulb_id = self.settings['api']['homeassistant']['bulb']['id']
        if activate:
            log.debug("TEAMFLASH!!")
            lightswitch.switch(bulb_id, 'turn_on', 1) 
            bulb_state = lightswitch.get_states(bulb_id) 
            log.debug(bulb_state)
        else:
            log.debug("STOP FLASHING ME!")
            lightswitch.switch(bulb_id, 'turn_off', 1) 
            bulb_state = lightswitch.get_states(bulb_id) 
            log.debug(bulb_state)

    def dacInfo(self, msg="ping"):
        self.txtLogInput.clear()
        self.txtLogInput.append(str(msg))
        log.info("Sent to ui log: {}".format(msg))

    def dacCloseApplication(self):
        log.info("Application closed")
        sys.exit()

