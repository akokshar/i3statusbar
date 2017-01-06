
from threading import Lock 
from pulsectl import Pulse, PulseLoopStop

from Logger import Logger
from Worker import Worker

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class PulseClient(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.pulseCallLock = Lock()
        self.pulseListenLock = Lock()

        self.pulse = Pulse('PulseClient')
        self.pulse.module_load('module-switch-on-connect')

        self.pulse.event_callback_set(self.pulseEventCallback)
        self.pulse.event_mask_set('sink', 'source', 'card')
        #self.pulse.event_mask_set('all')

        self.sinkEventCallback = None
        self.sourceEventCallback = None 

        self.worker = Worker()
        self.worker.setIdleCallback(self.onWorkerIdle)
        #self.onWorkerIdle()
        self.worker.start()

    def stop(self):
        pass

    def setSinkEventCallback(self, callback):
        self.sinkEventCallback = callback

    def setSourceEventCallback(self, callback):
        self.sourceEventCallback = callback

    def onWorkerIdle(self, **args):
        #Logger.logMessage("workerIdleCallback!!!")
        self.worker.addJob(self.pulseListen)

    def pulseListen(self, **args):
        self.pulseCallLock.acquire()
        self.pulseListenLock.acquire()
        self.pulseCallLock.release()
        self.pulse.event_listen()
        self.pulseListenLock.release()

    def pulseEventCallback(self, event):
        #Logger.logMessage("pulseEventCallback!!!: {0}".format(event))
        if event.facility == "sink":
            self.worker.addJob(self.sinkEventCallback, facility='sink')
        elif event.facility == "source":
            self.worker.addJob(self.sourceEventCallback, facility='source')
        else:
            self.worker.addJob(self.muteAll)
        raise PulseLoopStop

    def _doPulseCall(self, func, **args):
        self.pulseCallLock.acquire()
        self.pulse.event_listen_stop()
        self.pulseListenLock.acquire()
        self.pulseListenLock.release()
        result = func(**args)
        self.pulseCallLock.release()
        return result

    def getDefaultSink(self):
        for sink in self.pulse.sink_list():
            if sink.name == self.pulse.server_info().default_sink_name:
                return sink

    def getDefaultSource(self):
        for source in self.pulse.source_list():
            if source.name == self.pulse.server_info().default_source_name:
                return source

    def _doMuteAllSinks(self, **args):
        for sink in self.pulse.sink_list():
            self.pulse.mute(sink, mute = True)

    def muteAllSinks(self):
        self._doPulseCall(self._doMuteAllSinks)

    def _doMuteAllSources(self, **args):
        for source in self.pulse.source_list():
            self.pulse.mute(source, mute = True)

    def muteAllSources(self):
        self._doPulseCall(self._doMuteAllSources)

    def muteAll(self):
        self.muteAllSinks()
        self.muteAllSources()

    #####

    def _doGetDefaultSinkMute(self, **args):
        #Logger.logMessage("sink mute={0}".format(self.getDefaultSink().mute))
        return self.getDefaultSink().mute == 1

    def getDefaultSinkMute(self):
        return self._doPulseCall(self._doGetDefaultSinkMute)

    def _doSetDefaultSinkMute(self, **args):
        #Logger.logMessage("_doSetDefaultSinkMute")
        self.pulse.mute(self.getDefaultSink(), mute=args["mute"])
    
    def setDefaultSinkMute(self, mute):
        self._doPulseCall(self._doSetDefaultSinkMute, mute=mute)

    #####

    def _doGetDefaultSourceMute(self, **args):
        #Logger.logMessage("source  mute={0}".format(self.getDefaultSource().mute))
        return self.getDefaultSource().mute == 1

    def getDefaultSourceMute(self):
        return self._doPulseCall(self._doGetDefaultSourceMute)

    def _doSetDefaultSourceMute(self, **args):
        #Logger.logMessage("_doSetDefaultSourceMute")
        self.pulse.mute(self.getDefaultSource(), mute=args["mute"])
    
    def setDefaultSourceMute(self, mute):
        self._doPulseCall(self._doSetDefaultSourceMute, mute=mute)

    #####

    def _doGetDefaultSinkVolume(self, **args):
        return self.pulse.volume_get_all_chans(self.getDefaultSink())

    def getDefaultSinkVolume(self):
        return self._doPulseCall(self._doGetDefaultSinkVolume)

    def _doSetDefaultSinkVolume(self, **args):
        self.pulse.volume_set_all_chans(self.getDefaultSink(), args["value"])

    def setDefaultSinkVolume(self, value):
        self._doPulseCall(self._doSetDefaultSinkVolume, value=value)

    #####

    def _doGetDefaultSourceVolume(self, **args):
        return self.pulse.volume_get_all_chans(self.getDefaultSource())

    def getDefaultSourceVolume(self):
        return self._doPulseCall(self._doGetDefaultSourceVolume)

    def _doSetDefaultSourceVolume(self, **args):
        self.pulse.volume_set_all_chans(self.getDefaultSource(), args["value"])

    def setDefaultSourceVolume(self, value):
        self._doPulseCall(self._doSetDefaultSourceVolume, value=value)

