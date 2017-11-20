# -*- coding: utf-8 -*-

from threading import Timer

from Logger import Logger
from StatusLineControl import StatusLineControl
from StatusLineBlock import StatusLineBlock

class StatusLineSlider(StatusLineControl):

    def __init__(self, name, label):
        StatusLineControl.__init__(self, name)

        self.caption = label
        self.separator_width = 9
        self._value = 0
        self.step = 1

        self.label = StatusLineBlock(self.getFormattedLable())
        self.label.name = name
        self.label.instance = "label"
        self.label.separator = False
        self.label.separator_block_width = self.separator_width

        self.dec = StatusLineBlock("❰")
        #self.dec = StatusLineBlock("<span size='small'>❰</span>")
        #self.dec.markup = "pango"
        self.dec.name = name
        self.dec.instance = "dec"
        self.dec.separator = False
        self.dec.separator_block_width = 0

        self.lenght = 25
        self.slider = []
        for i in range(0, self.lenght + 1):
            slider = StatusLineBlock("•")
            #slider = StatusLineBlock("<span size='small'>•</span>")
            #slider.markup = "pango"
            slider.name = name
            slider.color = None
            slider.instance = int(i * 100 / self.lenght)
            slider.separator = False
            slider.separator_block_width = 0
            self.slider.append(slider)

        self.inc = StatusLineBlock("❱ ")
        #self.inc = StatusLineBlock("<span size='small'>❱</span>")
        #self.inc.markup = "pango"
        self.inc.name = name
        self.inc.instance = "inc"
        self.inc.separator = False
        self.inc.separator_block_width = self.separator_width

        self.value = 0

    @property
    def color(self):
        return self.label.color

    @color.setter
    def color(self, color):
        if not self.label.color == color:
            self.label.color = color
            self.update()

    @property
    def border(self):
        return self.label.border

    @border.setter
    def border(self, color):
        if not self.label.border == color:
            self.label.border = color
            self.dec.border = color
            for point in self.slider:
                point.border = color
            self.inc.border = color

            self.update()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value < 0: value = 0
        if value > 100: value = 100

        if not int(value) == self._value:
            oldIndex = self._value*self.lenght/100
            self._value = int(value)
            newIndex = self.value*self.lenght/100

            if not oldIndex == newIndex:
                i = 0
                if self.value > 0:
                    while i <= newIndex:
                        self.slider[i].color = "#FF0000"
                        i += 1

                while i <= self.lenght:
                    self.slider[i].color = None
                    i += 1

            self.label.full_text = self.getFormattedLable()
            self.update()

    def getFormattedLable(self):
        return " {0}{1}% ".format(self.caption, self.value)

    def changeValue(self, value):
        oldValue = self.value
        self.value = value
        if not oldValue == self.value:
            self.doChangeValue(self.value)

    @property
    def blocks(self):
        yield self.label
        if self.isActive:
            yield self.dec
            # Logger.logMessage(" {0} show slider".format(self.name))
            for point in self.slider:
                yield point
            yield self.inc

    def doOnScrollDown(self, event):
        self.changeValue(self.value - self.step)

    def doOnScrollUp(self, event):
        self.changeValue(self.value + self.step)

    def doOnLeftClick(self, event):
        if "instance" in event:
            if event["instance"] == "label":
                self.isActive = not self.isActive
            elif event["instance"] == "inc":
                self.changeValue(self.value + self.step)
            elif event["instance"] == "dec":
                self.changeValue(self.value - self.step)
            else:
                try:
                    value = int(event["instance"])
                    self.changeValue(value)
                except:
                    pass

    def doOnClick(self, event):
        return

    def doChangeValue(self, newValue):
        pass

    def doOnActivate(self):
        Logger.logMessage("Slider {0} expanded".format(self.name))
        self.label.separator_block_width = 0
#        self.label.separator = False

    def doOnDeactivate(self):
        Logger.logMessage("Slider {0} collapsed".format(self.name))
        self.label.separator_block_width = self.separator_width
#        self.label.separator = True
