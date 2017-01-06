from Logger import Logger
from threading import Timer

class StatusLineControl(object):
    'base class for status line controls.'
    
    def __init__(self, name):
        self._isActive = False
        self.refreshCallback = None
        self._name = name

        self.deactivateTimer = None
        self.deactivateTimeout = 3

    @property
    def name(self):
        return self._name

    @property
    def blocks(self):
        pass
    
    def setRefreshCallback(self, callback):
        self.refreshCallback = callback

    def update(self):
        self.doOnUpdate()
        self.refresh()
        self.doOnUpdateDone()
    
    def refresh(self):
        if self.refreshCallback != None:
            self.refreshCallback()

    def scheduleUpdate(self, interval):
       self.timer = Timer(interval, self.update)
       self.timer.start()

    @property
    def isActive(self):
        return self._isActive

    @isActive.setter
    def isActive(self, value):
        if self._isActive == value:
            return
        
        #Logger.logMessage("active.setter")
        
        self._isActive = value
        if self._isActive == True:
            self.doOnActivate()
        else:
            if self.deactivateTimer != None:
                self.deactivateTimer.cancel()
            self.doOnDeactivate()

        self.update()

    def onDeactivateTimeout(self):
        self.isActive = False
        self.update()
        #self.scheduleUpdate(0)

    def clicked(self, event):
        #Logger.logMessage("clicked")
        if self.deactivateTimer != None:
            self.deactivateTimer.cancel()
        self.deactivateTimer = Timer(self.deactivateTimeout, self.onDeactivateTimeout)
        self.deactivateTimer.start()

        self.doOnClick(event)

        if event["button"] == 1:
            self.doOnLeftClick(event)
        elif event["button"] == 2:
            self.doOnMiddleClick(event)
        elif event["button"] == 3:
            self.doOnRightClick(event)
        elif event["button"] == 4:
            self.doOnScrollDown(event)
        elif event["button"] == 5:
            self.doOnScrollUp(event)

    def doOnClick(self, event):
        pass

    def doOnRightClick(self, event):
        pass

    def doOnMiddleClick(self, event):
        pass

    def doOnLeftClick(self, event):
        pass

    def doOnScrollDown(self, event):
        pass

    def doOnScrollUp(self, event):
        pass

    def doOnUpdate(self):
        pass

    def doOnUpdateDone(self):
        pass
    
    def doOnActivate(self):
        pass

    def doOnDeactivate(self):
        pass
