import threading
from collections import deque

from Logger import Logger

class Worker(threading.Thread):
    'An infinite thread to execute jobs on'

    def __init__(self, **args):
        threading.Thread.__init__(self)
        #if args.has_key("idleCallBack"):
        if "idleCallBack" in args:
            self.idleCallback = args["idleCallback"]
        else:
            self.idleCallback = None

        self.jobCount = 0
        self.work = deque()
        self.hasWork = threading.Semaphore(0)
        self.queueLock = threading.Lock()
        self._isRunning = True
#        self.start()

    def run(self):
        #while self.hasWork.acquire():
        while self._isRunning:
            #Logger.logMessage("queue len = {0}".format(self.jobCount))
            if self.jobCount == 0 and not self.idleCallback == None:
                self.idleCallback()
            
            self.hasWork.acquire()
            if not self._isRunning:
                return
            
            work = self.work.popleft()
            work[0](**work[1])
            self.jobCount -= 1

    def stop(self):
        self._isRunning = False
        self.hasWork.release()

    def setIdleCallback(self, idleCallback):
        self.idleCallback = idleCallback

    def addJob(self,job, **args):
        if job == None:
            return
        self.queueLock.acquire()
        self.work.append([job, args])
        self.jobCount += 1
        self.hasWork.release()
        self.queueLock.release()

