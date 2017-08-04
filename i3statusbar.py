#!/usr/bin/python3
# -*- coding: utf-8 -*-

import signal
import time
import json
from sys import stdin,stdout

from Logger import Logger
from StatusLine import StatusLine
from StatusLineLabel import StatusLineLabel 
from StatusLineDatetime import StatusLineDatetime
from StatusLineLanguage import StatusLineLanguage
from StatusLineBattery import StatusLineBattery
from StatusLineAC import StatusLineAC
from StatusLineCPU import StatusLineCPU
from StatusLineMemory import StatusLineMemory
from StatusLineBrightness import StatusLineBrightness
from StatusLineVolume import StatusLineVolume
from StatusLineCapture import StatusLineCapture
#from StatusLineNetworkManager import StatusLineNetworkManager

print('{"version":1,"click_events":true}')
print('[')

def printStatusLine(components):
    stdout.write(json.dumps(components) + ",\n")
    #Logger.logMessage(json.dumps(components))
    stdout.flush()

line = StatusLine(printStatusLine)
#line.addControl(StatusLineNetworkManager())
line.addControl(StatusLineMemory())
line.addControl(StatusLineCPU())
line.addControl(StatusLineAC())
line.addControl(StatusLineBattery("BAT0"))
line.addControl(StatusLineBattery("BAT1"))
line.addControl(StatusLineCapture())
line.addControl(StatusLineVolume())
line.addControl(StatusLineBrightness())
line.addControl(StatusLineDatetime())
line.addControl(StatusLineLanguage())

running = True

def onSigInt(sig, frame):
    running = False
    signal.alarm(1) # necessary to interrupt read from stdin

def onSigUsr1(sig, frame):
    line.refresh()
#    pass

signal.signal(signal.SIGINT, onSigInt)
signal.signal(signal.SIGUSR1, onSigUsr1)

while running:
    eventStr = stdin.readline()
    if not running:
        del line
        exit(0)
 
    try:
        event = json.loads(eventStr.strip(","))
        #Logger.logMessage(eventStr.strip(","))
        line.processEvent(event)
    except ValueError:
        pass

