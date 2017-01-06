#!/usr/bin/python

from PulseClient import PulseClient
from pulsectl import Pulse, PulseLoopStop

pulse1 = PulseClient()
pulse2 = PulseClient()
pulse3 = PulseClient()

state =pulse1.getDefaultSourceMute()  
if state == True:
    print "Muted"
else:
    print "Not muted"
pulse1.setDefaultSourceMute(not state)

exit(0)

"""
with Pulse('event-printer') as pulse:
    pulse.module_load('module-switch-on-connect')

    print pulse.event_types
    print pulse.event_facilities
    print pulse.event_masks

    def print_events(ev):
        print('Pulse event:', ev)
        ### Raise PulseLoopStop for event_listen() to return before timeout (if any)
        # raise PulseLoopStop

    pulse.event_mask_set('all')
    pulse.event_callback_set(print_events)
    pulse.event_listen(timeout=5)
"""
