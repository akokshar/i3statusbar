# -*- coding: utf-8 -*-

from subprocess import check_output, Popen, PIPE
import pyudev


from Logger import Logger
from StatusLineSlider import StatusLineSlider

class StatusLineBrightness(StatusLineSlider):

    def __init__(self):
        StatusLineSlider.__init__(self, "backlight", "🔆")

        #self.step = 2

        self.border = "#aec795"

        self.udevCtx = pyudev.Context()
        self.udevMon = pyudev.Monitor.from_netlink(self.udevCtx)
        self.udevMon.filter_by(subsystem='backlight')
        self.udevObs = pyudev.MonitorObserver(self.udevMon, callback=self.onUdevEvent)

        for device in self.udevCtx.list_devices(subsystem='backlight'):
            self.onUdevEvent(device)

        self.udevObs.start()

    def onUdevEvent(self, device):
        maxBrightness = device.attributes.asint('max_brightness')
        actualBrightness = device.attributes.asint('brightness')

        value = round(actualBrightness/(float(maxBrightness)/100))
        #Logger.logMessage("udev value {0} {1}".format(value, int(value)))
        self.value = value

    def doChangeValue(self, value):
        #Logger.logMessage("doOnChange to {0}".format(str(value)))
        backlight = Popen([
            '/usr/bin/xbacklight', 
            '-set', str(value), 
            '-steps', '1',
            '-time', '0'])
        
