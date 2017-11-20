# -*- coding: utf-8 -*-

from subprocess import check_output, Popen, PIPE
import shlex
import colorsys

from Logger import Logger
from StatusLineControl import StatusLineControl
from StatusLineBlock import StatusLineBlock

class StatusLineMemory(StatusLineControl):

    def __init__(self):
        StatusLineControl.__init__(self, "mem")
        self.updateInterval = 10

        self.memUsage = StatusLineBlock("")
        self.memUsage.min_width = "MEM 9.99G/99.9G"
        self.memUsage.align = "center"
        self.memUsage.border = "#CAD1DB"
        self.memUsage.separator = False

        self.scheduleUpdate(0)
  
    @property
    def blocks(self):
        yield self.memUsage

    def getMemTotal(self):
        memTotal = check_output([
            'awk', 
            '/^MemTotal:/ {total=$2} END { printf("%.1f", total/1024/1024) }',
            '/proc/meminfo'])
        return float(memTotal)
        
    def getMemAvailable(self):
        memAvailable = check_output([
            'awk', 
            '/^MemAvailable:/ {total=$2} END { printf("%.1f", total/1024/1024) }',
            '/proc/meminfo'])
        return float(memAvailable)

    def doOnUpdate(self):
        memTotal = self.getMemTotal()
        memAvailable = self.getMemAvailable()
        self.memUsage.full_text = " MEM {:.2f}G/{:.2f}G ".format(memAvailable, memTotal)

    def doOnUpdateDone(self):
        self.scheduleUpdate(self.updateInterval)
