from threading import Timer

from Logger import Logger

class StatusLine(object):
    def __init__(self, refreshCallback):
        self.lastClickedControl = None
        self.controls = {}
        self.orderedNames = []
        self.refreshCallback = refreshCallback

        self.timer = None

    def start(self):
        pass

    def stop(self):
        #TODO: stop all controls
        if self.timer != None and self.timer.is_alive():
            self.timer.cancel()

    def pause(self):
        pass

    def resume(slef):
        pass

    def addControl(self, control):
        name = control.name
        control.setRefreshCallback(self.onControlChange)
        self.orderedNames.append(name)
        self.controls[name] = control
        self.doUpdate()
   
    def doUpdate(self):
        #Logger.logMessage("update line")
        self.refreshCallback(list(self.blocks))

    def onControlChange(self):
        # do not update more then 10 times in a second
        if self.timer == None or not self.timer.is_alive():
            self.timer = Timer(0.1, self.doUpdate)
            self.timer.start()

    @property
    def blocks(self):
        for name in self.orderedNames:
            for block in self.controls[name].blocks:
                yield block.getAttrs()

    def processEvent(self, event):
        #Logger.logMessage("click event")

        if not event.has_key("name") or not self.controls.has_key(event["name"]):
            return


        clickedControl = self.controls[event["name"]]

        if self.lastClickedControl == None:
            self.lastClickedControl = clickedControl
            #self.lastClickedControl.isActive = True
        else:
            if self.lastClickedControl.name != clickedControl.name:
                #Logger.logMessage("change active control")
                self.lastClickedControl.isActive = False
                self.lastClickedControl = clickedControl
                #self.lastClickedControl.isActive = True
            
        self.lastClickedControl.clicked(event)
        
    def refresh(self):
        for name, control in self.controls.items():
            control.update()
