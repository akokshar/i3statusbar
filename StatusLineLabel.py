from Logger import Logger
from StatusLineControl import StatusLineControl
from StatusLineBlock import StatusLineBlock

class StatusLineLabel(StatusLineControl):

    def __init__(self, name, text):
        StatusLineControl.__init__(self, name)
        self.text = text
        self.label = StatusLineBlock(text)
        self.label.name = name
        self.count = 0
  
    @property
    def blocks(self):
        yield self.label

    def doOnActivate(self):
        #Logger.logMessage("doOnActivate")
        #self.label.color = "red"
        pass

    def doOnDeactivate(self):
        #Logger.logMessage("doOnDeactivate")
        #self.label.color = None
        pass

    def doOnUpdate(self):
        #Logger.logMessage("doOnUpdate")
        #self.count += 1
        #self.label.full_text = self.text + str(self.count)
        pass

    def doOnUpdateDone(self):
        #Logger.logMessage("doOnUpdateDone")
        pass
    
    def doOnClick(self, event):
        #self.isActive = True
        pass

