# -*- coding: utf-8 -*-

from subprocess import check_output, Popen, PIPE
import shlex
import colorsys
import pyudev

from Logger import Logger
from StatusLineControl import StatusLineControl
from StatusLineBlock import StatusLineBlock

class StatusLineBattery(StatusLineControl):

    def __init__(self, battery):
        StatusLineControl.__init__(self, battery)
        
        self.full = StatusLineBlock("{0} --.--%".format(self.name))
        self.full.name = self.name
        
        self.short = StatusLineBlock(" ")
        self.short.name = self.name
        
        self.udevCtx = pyudev.Context()
        self.udevMon = pyudev.Monitor.from_netlink(self.udevCtx)
        self.udevMon.filter_by(subsystem='power_supply')
        self.udevObs = pyudev.MonitorObserver(self.udevMon, callback=self.onUdevEvent)

        for device in self.udevCtx.list_devices(subsystem='power_supply'): 
            self.onUdevEvent(device)

        self.udevObs.start()
  
    @property
    def blocks(self):
        if self.isActive:
            yield self.full
        else:
            yield self.short

    def getBatteryCharge(self, device):
        now = device.attributes.asint('energy_now')
        full = device.attributes.asint('energy_full')
        return float(now)/full*100

    def onUdevEvent(self, device):
        Logger.logMessage("Udev for: {0} self:{1}".format(device.sys_name, self.name))
        if device.sys_name == self.name:
            Logger.logMessage("do change for: {0} self:{1}".format(device.sys_name, self.name))
            charge = self.getBatteryCharge(device)
            color = colorsys.hsv_to_rgb(1.0/360*120*(charge)/100, 0.5, 0.75)
            color = [int(c *255) for c in color]
            self.short.color = "#{0[0]:0>2x}{0[1]:0>2x}{0[2]:0>2x}".format(color)
            self.full.color = "#{0[0]:0>2x}{0[1]:0>2x}{0[2]:0>2x}".format(color)
            self.full.full_text = "{0} {1:.2f}%".format(device.sys_name, charge)

            self.update()

    def doOnLeftClick(self, event):
        self.isActive = not self.isActive


