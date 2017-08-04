# -*- coding: utf-8 -*-

from subprocess import check_output, Popen, PIPE
import shlex
import colorsys
import pyudev

from Logger import Logger
from StatusLineControl import StatusLineControl
from StatusLineBlock import StatusLineBlock

class StatusLineAC(StatusLineControl):

    def __init__(self):
        StatusLineControl.__init__(self, "AC")

        self.acLabel = StatusLineBlock("")
        self.acLabel.separator = False
        
        self.udevCtx = pyudev.Context()
        self.udevMon = pyudev.Monitor.from_netlink(self.udevCtx)
        self.udevMon.filter_by(subsystem='power_supply')
        self.udevObs = pyudev.MonitorObserver(self.udevMon, callback=self.onUdevEvent)
        
        for device in self.udevCtx.list_devices(subsystem='power_supply'):
            self.onUdevEvent(device)

        self.udevObs.start()

    @property
    def blocks(self):
        if self.isACOnline:
            yield self.acLabel

    def onUdevEvent(self, device):
        #Logger.logMessage(device.sys_name)
        if device.sys_name == self.name:
            self.isACOnline = device.attributes.asbool('online')
            self.update()

    def doOnUpdate(self):
        pass

    def doOnUpdateDone(self):
        pass
