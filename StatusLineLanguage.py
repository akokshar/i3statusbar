from Logger import Logger
from Worker import Worker
from StatusLineControl import StatusLineControl
from StatusLineBlock import StatusLineBlock

from ctypes import *

_libX11=CDLL('libX11.so.6')

class Display(Structure):
    pass

XkbOpenDisplay = _libX11.XkbOpenDisplay
XkbOpenDisplay.restype = POINTER(Display)
XkbOpenDisplay.argtypes = [
        c_char_p,       # display_name 
        POINTER(c_int), # event_rtrn
        POINTER(c_int), # error_rtrn
        POINTER(c_int), # major_in_out
        POINTER(c_int), # minor_in_out
        POINTER(c_int)  # reason_rtrn
        ]

#/usr/include/X11/extensions/XKB.h:#define	XkbUseCoreKbd		0x0100
XkbUseCoreKbd = 0x0100

#/usr/include/X11/extensions/XKB.h:#define	XkbStateNotify			2
XkbStateNotify = 2

#/usr/include/X11/extensions/XKB.h:#define	XkbGroupStateMask		(1L << 4)
XkbGroupStateMask = (1<<4)

#/usr/include/X11/extensions/XKB.h:#define	XkbModifierStateMask		(1L << 0)
XkbModifierStateMask = (1<<0)

XkbSelectEventDetails = _libX11.XkbSelectEventDetails
XkbSelectEventDetails.restype = c_bool
XkbSelectEventDetails.argtypes = [
        POINTER(Display),
        c_uint, # device_spec
        c_uint, # event_type
        c_ulong, # bits_to_change
        c_ulong  # values_for_bits
        ]

class XEvent(Union):
    _fields_ = [
            ("type", c_int),
            ("pad", c_long)
            ]

class XkbAnyEvent(Structure):
    _fields_ = [
            ("type", c_int),
            ("serial", c_ulong),
            ("send_event", c_bool),
            ("display", POINTER(Display)),
            ("time", c_long), # Time long??! (sizeof Time:8, long:8, int=4)
            ("xkb_type", c_int),
            ("device", c_uint)
            ]

class XkbStateNotifyEvent(Structure):
    _fields_ = [
            ("type", c_int),
            ("serial", c_ulong),
            ("send_event", c_bool),
            ("display", POINTER(Display)),
            ("time", c_long), # Time long??! (sizeof Time:8, long:8, int=4)
            ("xkb_type", c_int),
            ("device", c_uint),
            ("changed", c_uint), #mask of changed state components
            ("group", c_int), #keyboard group
            ("base_group", c_int), #base keyboard group
            ("latched_group", c_int), #latched keyboard group
            ("locked_group", c_int), #locked keyboard group
            ("mods", c_uint), #modifiers state
            ("base_mods", c_uint), #base modifiers state
            ("latched_mods", c_uint), #latched modifiers 
            ("locked_mods", c_uint), #locked modifiers
            ("compat_state", c_int), #compatibility state
            ("grab_mods", c_uint), #mods used for grabs
            ("compat_grab_mods", c_uint), #grab mods for non-XKB clients
            ("lookups_mods", c_uint), #mods sent to clients
            ("compat_lookup_mods", c_uint), #mods sent to non-XKB clients
            ("ptr_buttons", c_int), #pointer putton state
            ("keycode", c_ubyte), #keycode that caused the change (KeyCode type)
            ("event_type", c_char), #KeyPress or KeyRelease
            ("req_major", c_char), #Major opcode of request
            ("req_minor", c_char)  #Minor opcode of request
            ]

class XkbEvent(Union):
    _fields_ = [
            ("type", c_int),
            ("any", XkbAnyEvent),
            ("state", XkbStateNotifyEvent),
            ("core", XEvent)
            ]

XNextEvent = _libX11.XNextEvent
XNextEvent.restype = c_int
XNextEvent.argtypes = [
        POINTER(Display),
        POINTER(XEvent)
        ]

class StatusLineLanguage(StatusLineControl):

    def __init__(self):
        StatusLineControl.__init__(self, "lang")
        self.label = StatusLineBlock("--")
        self.label.name = self.name

        self.indicators = ["en", "ru"]
    
        self.xkbEventType = c_int(0)
        error = c_int(0)
        reason = c_int(0)

        self.display = XkbOpenDisplay(None, byref(self.xkbEventType), byref(error), None, None, byref(reason))
        if not self.display:
            self.label.full_text = "Error (OpenDisplay)"
            return

        select = XkbSelectEventDetails(self.display, XkbUseCoreKbd, XkbStateNotify, (XkbGroupStateMask|XkbModifierStateMask), (XkbGroupStateMask|XkbModifierStateMask))
        if not select:
            self.label.full_text = "Error (SelectEvent)"
            return

        self.worker = Worker()
        self.worker.addJob(self.readXkbEvents)
        self.worker.start()

    def readXkbEvents(self):
        """
        Read an process XkbEvents. Will block forever.
        """
        event = XkbEvent()
        while True:
            XNextEvent(self.display, event.core)
            if event.type == self.xkbEventType.value and event.any.xkb_type == XkbStateNotify:
                if event.state.group >= len(self.indicators):
                    return
                indicator = self.indicators[event.state.group]
                
                caps = False
                if not ((event.state.mods & (1<<0)) == 0): #Shift
                    caps = not caps
                if not ((event.state.mods & (1<<1)) == 0): #CapsLock
                    caps = not caps

                if caps:
                    indicator = indicator.upper()
                
                if not self.label.full_text == indicator:
                    self.label.full_text = indicator
                    self.update()

                    #print("Yay {0}, {1}".format(event.state.mods , self.label.full_text))

    @property
    def blocks(self):
        yield self.label

    def doOnLeftClick(self, event):
        pass

if __name__ == "__main__":
    control = StatusLineLanguage()
    
    import json
    for block in control.blocks:
        print("{0}\n".format(json.dumps(block.getAttrs())))

    control.readXkbEvents()

    exit(0)

