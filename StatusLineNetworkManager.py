# -*- coding: utf-8 -*-

from Logger import Logger
from StatusLineControl import StatusLineControl
from StatusLineBlock import StatusLineBlock

import NetworkManager

class StatusLineNetworkManager(StatusLineControl):

    def __init__(self):
        StatusLineControl.__init__(self, "nm")

        self.wifiLabel = StatusLineBlock(" ")
        self.wifiLabel.name = self.name

    @property
    def blocks(self):
        yield self.wifiLabel

    def onStateChange(self):
       for connection in NetworkManager.NetworkManager.ActiveConnections:
           pass

    def doOnLeftClick(self, event):
        self.isActive = not self.isActive

    def doOnActivate(self):
        self.wifiLabel.full_text = NetworkManager.const('state', NetworkManager.NetworkManager.State)

    def doOnDeactivate(self):
        self.wifiLabel.full_text = " "
    

"""

https://github.com/seveas/python-networkmanager/tree/master/examples

import NetworkManager

c = NetworkManager.const
c('state', NetworkManager.NetworkManager.State)

for conn in NetworkManager.NetworkManager.ActiveConnections:
    settings = conn.Connection.GetSettings()['connection']
    print("%-30s %-20s %-10s %s" % (settings['id'], settings['type'], conn.Default, ", ".join([x.Interface for x in conn.Devices])))

... 
Red Hat Guest 1                802-11-wireless      False      wlp3s0
enp0s25                        802-3-ethernet       True       enp0s25


for conn in NetworkManager.NetworkManager.ActiveConnections:
    for dev in conn.Devices:
        for addr in dev.Ip4Config.Addresses:
            print("         %s/%d -> %s" % tuple(addr))

... 
         10.200.137.52/22 -> 10.200.139.254
         10.34.27.77/23 -> 10.34.27.254


"""
