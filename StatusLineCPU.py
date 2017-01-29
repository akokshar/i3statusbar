# -*- coding: utf-8 -*-

from subprocess import check_output, Popen, PIPE
import shlex
import colorsys

from Logger import Logger
from StatusLineControl import StatusLineControl
from StatusLineBlock import StatusLineBlock

class StatusLineCPU(StatusLineControl):

    def __init__(self):
        StatusLineControl.__init__(self, "cpu")
        self.updateInterval = 5

        self.cpuUsage = StatusLineBlock(" -----%")

        self.scheduleUpdate(0)
  
    @property
    def blocks(self):
        yield self.cpuUsage

    def getCPUIdle(self):
        try:
            mpstat = Popen([
               'mpstat', '1', '1'], stdout=PIPE)
            idleStr = check_output([
                'awk',
                '/^Average:/ {idle=$12} END {print idle}'
                ], stdin=mpstat.stdout)
            mpstat.stdout.close()
            return float(idleStr)
        except:
            return None

    def doOnUpdate(self):
        idle = self.getCPUIdle()
        if idle != None:
            color = colorsys.hsv_to_rgb(1.0/360*120*idle/100, 1, 1)
            color = [int(c *255) for c in color]

            self.cpuUsage.color = "#{0[0]:0>2x}{0[1]:0>2x}{0[2]:0>2x}".format(color)
            self.cpuUsage.full_text = " {:0>5.2f}%".format(100 - idle)
        else:
            self.cpuUsage.color = "red"
            self.cpuUsage.full_text = " {:s}".format("-----%")

    def doOnUpdateDone(self):
        self.scheduleUpdate(self.updateInterval)
