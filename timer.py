#!/bin/python

import time

import pyudev

context = pyudev.Context()
for device in context.list_devices(subsystem='sound'):
    print("{0} ({1})".format(device, device.device_type))

monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='sound')

def log_event(device):
     print('{0} {1}'.format(device.attributes.asstring('type'), device.sys_name))

observer = pyudev.MonitorObserver(monitor, callback=log_event, name='monitor-observer')
observer.start()

val = 30
for i in range(0, 26):
    print i, val/4


def testFunc(arg1, **args):
    print arg1
    for key in args:
        print key + "=" + args[key]

def testFunc1(**args):
   print args
   testFunc("test",** args)

#testFunc1(a='test', b='test')
testFunc("test")

print "Sleep"
time.sleep(5)
