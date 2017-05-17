# -*- coding: utf-8 -*-

from threading import Timer

from Logger import Logger
from StatusLineControl import StatusLineControl
from StatusLineBlock import StatusLineBlock

class StatusLineSlider(StatusLineControl):

    def __init__(self, name, label):
        StatusLineControl.__init__(self, name)

        self.label = StatusLineBlock(label)
        self.label.name = name
        self.label.instance = "label"
        self.label.separator = False
        self.label.separator_block_width = 3

        self.dec = StatusLineBlock("<span size='small'>❰</span>")
        self.dec.markup = "pango"
        self.dec.name = name
        self.dec.instance = "dec"
        self.dec.separator = False
        self.dec.separator_block_width = 3

        self.step = 1

        self._value = 0

        self.lenght = 25
        self.slider = []
        for i in range(0, self.lenght + 1):
            slider = StatusLineBlock("<span size='small'>•</span>")
            slider.markup = "pango"
            slider.name = name
            slider.instance = int(i * 100 / self.lenght)
            slider.separator = False
            slider.separator_block_width = 3
            self.slider.append(slider)

        self.inc = StatusLineBlock("<span size='small'>❱</span>")
        self.inc.markup = "pango"
        self.inc.name = name
        self.inc.instance = "inc"

        self.percent = StatusLineBlock("0%")
        self.percent.name = name
        self.percent.instance = "label"
        self.percent.separator = True
        self.percent.separator_block_width = 13

    @property
    def color(self):
        return self.label.color

    @color.setter
    def color(self, color):
        if not self.label.color == color:
            self.label.color = color
            self.percent.color = color
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
                        self.slider[i].color = "red"
                        i += 1

                while i <= self.lenght:
                    self.slider[i].color = None
                    i += 1

            self.percent.full_text = "{0}%".format(self.value)
            self.update()

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
            for point in self.slider:
                yield point
            yield self.inc
        else:
            yield self.percent

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

#    def doOnActivate(self):
#        self.label.separator = False

#    def doOnDeactivate(self):
#        self.label.separator = True
