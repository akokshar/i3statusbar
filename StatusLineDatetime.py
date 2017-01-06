# -*- coding: utf-8 -*-

from datetime import datetime
from threading import Timer

from Logger import Logger
from StatusLineControl import StatusLineControl
from StatusLineBlock import StatusLineBlock

class StatusLineDatetime(StatusLineControl):

    def __init__(self):
        StatusLineControl.__init__(self, "datetime")
        self.updateInterval = 15
        self.label = StatusLineBlock("")
        self.scheduleUpdate(0)
  
    @property
    def blocks(self):
        yield self.label

    def doOnUpdate(self):
        now = datetime.now()
        self.label.full_text =  now.strftime("%a %d %b %H:%M:%S")
        self.label.short_text = now.strftime("%H:%M")

    def doOnUpdateDone(self):
        self.scheduleUpdate(self.updateInterval)

