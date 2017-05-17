from Logger import Logger
from StatusLineControl import StatusLineControl
from StatusLineBlock import StatusLineBlock

from xkbgroup import XKeyboard

class StatusLineLanguage(StatusLineControl):

    def __init__(self):
        StatusLineControl.__init__(self, "lang")
        self.xkb = XKeyboard()
        self.label = StatusLineBlock("--")
        self.label.name = self.name
  
    @property
    def blocks(self):
        yield self.label

    def setLabel(self):
        if self.xkb.group_name.startswith("Eng"):
            self.label.full_text = "US"
        elif self.xkb.group_name.startswith("Rus"):
            self.label.full_text = "RU"

    def doOnLeftClick(self, event):
        Logger.logMessage("doOnLeftClick")
        self.setLabel()

    def doOnUpdate(self):
        self.setLabel()
