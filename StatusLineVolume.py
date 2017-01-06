# -*- coding: utf-8 -*-

from subprocess import check_output, Popen, PIPE
import pyudev
from pulsectl import Pulse, PulseLoopStop

from Logger import Logger
from Worker import Worker
from StatusLineSlider import StatusLineSlider
from PulseClient import PulseClient

class StatusLineVolume(StatusLineSlider):

    def __init__(self):
        StatusLineSlider.__init__(self, "volume", "🎵")

        self.step = 1

        self.pulseClient = PulseClient()
        self.pulseClient.setSinkEventCallback(self.pulseSinkEventCallback)
        self.pulseClient.setDefaultSinkMute(True)
        self.pulseSinkEventCallback()

    def pulseSinkEventCallback(self, **args):
        Logger.logMessage("pulseSinkEventCallback")
        volume = self.pulseClient.getDefaultSinkVolume()
        self.value = round(volume * 100)
        self.setMuteColor()

    def doChangeValue(self, value):
        volume = value/100.0
        self.pulseClient.setDefaultSinkVolume(volume)

    def doOnMiddleClick(self, event):
        mute = self.pulseClient.getDefaultSinkMute()  
        self.pulseClient.setDefaultSinkMute(not mute)
        self.setMuteColor()

    def setMuteColor(self):
        if self.pulseClient.getDefaultSinkMute() == True:
            self.color = '#676E7D'
        else:
            self.color = None

