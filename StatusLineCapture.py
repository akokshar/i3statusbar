# -*- coding: utf-8 -*-

from subprocess import Popen
import pyudev
from pulsectl import Pulse, PulseLoopStop

from Logger import Logger
from Worker import Worker
from StatusLineSlider import StatusLineSlider
from PulseClient import PulseClient

class StatusLineCapture(StatusLineSlider):

    def __init__(self):
        StatusLineSlider.__init__(self, "capture", "🎤")

        self.step = 1

        self.border = "#ae95c7"

        self.pulseClient = PulseClient()
        self.pulseClient.setSourceEventCallback(self.pulseSourceEventCallback)
        self.pulseClient.setDefaultSourceMute(True)
        self.pulseSourceEventCallback()

    def pulseSourceEventCallback(self, **args):
        volume = self.pulseClient.getDefaultSourceVolume()
        self.value = round(volume * 100)
        self.setColor()

    def doChangeValue(self, value):
        volume = value/100.0
        self.pulseClient.setDefaultSourceVolume(volume)

    def doOnRightClick(self, event):
        mute = self.pulseClient.getDefaultSourceMute()  
        self.pulseClient.setDefaultSourceMute(not mute)
        self.setColor()

    def doOnMiddleClick(self, event):
        Popen(["/usr/bin/pavucontrol", "--tab", "4"])

    def setColor(self):
        if self.pulseClient.getDefaultSourceMute() == True:
            self.color = '#676E7D'
        else:
            self.color = None


