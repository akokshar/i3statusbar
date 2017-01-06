# -*- coding: utf-8 -*-

from subprocess import check_output, Popen, PIPE
import shlex
import colorsys
import pyudev

from Logger import Logger
from StatusLineControl import StatusLineControl
from StatusLineBlock import StatusLineBlock

# 🔋

class StatusLineBattery(StatusLineControl):

    def __init__(self):
        StatusLineControl.__init__(self, "BAT")

        self.bat = {}
        self.bat["BAT0"] = StatusLineBlock("BAT0 --.--%")
        self.bat["BAT1"] = StatusLineBlock("🔋 --.--%")
        
        self.udevCtx = pyudev.Context()
        self.udevMon = pyudev.Monitor.from_netlink(self.udevCtx)
        self.udevMon.filter_by(subsystem='power_supply')
        self.udevObs = pyudev.MonitorObserver(self.udevMon, callback=self.onUdevEvent)

        for device in self.udevCtx.list_devices(subsystem='power_supply'): 
            self.onUdevEvent(device)

        self.udevObs.start()
  
    @property
    def blocks(self):
        yield self.bat["BAT0"]
        yield self.bat["BAT1"]

    def getBatteryCharge(self, device):
        now = device.attributes.asint('energy_now')
        full = device.attributes.asint('energy_full')
        return float(now)/full*100

    def onUdevEvent(self, device):
        if device.sys_name == "BAT0" or device.sys_name == "BAT1":
            charge = self.getBatteryCharge(device)
            color = colorsys.hsv_to_rgb(1.0/360*120*(charge)/100, 1, 1)
            color = [int(c *255) for c in color]
            self.bat[device.sys_name].color = "#{0[0]:0>2x}{0[1]:0>2x}{0[2]:0>2x}".format(color)
            self.bat[device.sys_name].full_text = "{0} {1:.2f}%".format(device.sys_name, charge)

    def doOnUpdate(self):
        pass

    def doOnUpdateDone(self):
        pass
