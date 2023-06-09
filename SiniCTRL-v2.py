#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import paho.mqtt.client as mqtt 

import time

#------------------------------------------------------------------------------
# MQTT Stuffz
#------------------------------------------------------------------------------

#--------------------------------------
# Specific to MY network
# These are MY SiniLink USB switches
#--------------------------------------
mqttBroker ="Skynet"

WindowTitle = "SiniLink CTRLs"

# The device data as a "structure"
S_Devices = [
    # Device         Operation   State
    ["SiniLink_0",   "Power",   "wtf"],
    ["SiniLink_1",   "Power00", "wtf"],
    ["SiniLink_2",   "Power",   "wtf"],
    ["SiniLink_3",   "Power",   "wtf"],
    ["BoolSharts",   "Power",   "wtf"]
]

Device_0 = "SiniLink_0"
Device_1 = "SiniLink_1"
Device_2 = "SiniLink_2"
Device_3 = "SiniLink_3"

Part_0 = "Power"
Part_1 = "Power00"      # This one's different because it's a newer version of the firmware
Part_2 = "Power"
Part_3 = "Power"

State_0 = "wtf"
State_1 = "wtf"
State_2 = "wtf"
State_3 = "wtf"

client_id = f'SiniLink_Controls-{time.time()}'
# This needs to be made unique if you might run more than one instance...
# I'm actually using "seconds since epoc" as a differentiator.
# Of course, it'd be even better to figure out how to actually confirm that
# there isn't already a device with this exact name connected to the broker.

lwt_topic = "LWT/"+client_id
#--------------------------------------

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
        print(client_id, "is connected to", mqttBroker)
        #--------------------------------------
        print("Subscribed to:")
        for x in range(0, len(S_Devices)):
            client.subscribe("stat/"+S_Devices[x][0]+"/"+S_Devices[x][1], 0)
            print("\tstat/"+S_Devices[x][0]+"/"+S_Devices[x][1])

        ######################################################
        print("DURING MQTT Connect!")
        print("Requesting status of:")
        for x in range(0, len(S_Devices)):
            print("\t"+S_Devices[x][0]+"\t"+S_Devices[x][1])
            client.publish("cmnd/"+S_Devices[x][0]+"/"+"Status", S_Devices[x][1])
        ######################################################

        #--------------------------------------
    else:
        print("Bad connection Returned code=",rc)

def on_message(client, userdata, message):
    #--------------------------------------
    #--------------------------------------
    global S_Devices

    print("  topic:", message.topic)
    print("message:", str(message.payload.decode("utf-8")))

    for x in range(0, len(S_Devices)):
        if(message.topic == "stat/"+S_Devices[x][0]+"/"+S_Devices[x][1]):
            S_Devices[x][2] = str(message.payload.decode("utf-8"))

    # for x in range(0, len(S_Devices)):
    #     print(x, S_Devices[x][2])

client = mqtt.Client(client_id)
client.will_set(lwt_topic, payload="(I B ded)")

client.on_connect=on_connect    #bind call back function
client.on_message=on_message    #attach function to callback

#------------------------------------------------------------------------------
# The Window!
#------------------------------------------------------------------------------

class TOGGLE_WINDOW:

    def destroy(self, widget, data=None):
        print('destroy event occurred (i.e.: Window was closed...)')
        print(">>> 666 <<<", S_Devices[0][2], S_Devices[1][2], S_Devices[2][2], S_Devices[3][2])
        Gtk.main_quit()

    #--------------------------------------
    # Build the window
    #--------------------------------------
    def __init__(self):

        ######################################################
        print("DURING Window Init!")
        print("Requesting status of:")
        for x in range(0, len(S_Devices)):
            print("\t"+S_Devices[x][0]+"\t"+S_Devices[x][1])
            client.publish("cmnd/"+S_Devices[x][0]+"/"+"Status", S_Devices[x][1])
        ######################################################

# So...
# How do I get it to wait here until I have responses to those "Status" commands?
# hhhmmm...
        # print(State_0, State_1, State_2, State_3)

        Label_0 = S_Devices[0][0]+' - '+S_Devices[0][2]
        Label_1 = S_Devices[1][0]+' - '+S_Devices[1][2]
        Label_2 = S_Devices[2][0]+' - '+S_Devices[2][2]
        Label_3 = S_Devices[3][0]+' - '+S_Devices[3][2]

        print(Label_0, Label_1, Label_2, Label_3)
        print(">>> 1 <<<", S_Devices[0][2], S_Devices[1][2], S_Devices[2][2], S_Devices[3][2])
        ######################################################

        TheWindow = Gtk.Window()
        TheWindow.set_position(Gtk.WindowPosition.CENTER)
        TheWindow.set_title(WindowTitle)
        TheWindow.connect('destroy', self.destroy)

        #--------------------------------------
        # One of the truly FUGLY parts...
        # Should figure out how to turn it into
        # a loop.  Maybe build up an array or
        # structure to define the devices
        #--------------------------------------
        self.toggle0 = Gtk.ToggleButton(label = Label_0)
        self.toggle0.connect('toggled', self.on_toggled0, 'toggle')
        self.toggle0.set_size_request(200, 0)

        self.toggle1 = Gtk.ToggleButton(label = Label_1)
        self.toggle1.connect('toggled', self.on_toggled1, 'toggle')
        self.toggle0.set_size_request(200, 0)

        self.toggle2 = Gtk.ToggleButton(label = Label_2)
        self.toggle2.connect('toggled', self.on_toggled2, 'toggle')
        self.toggle0.set_size_request(200, 0)

        self.toggle3 = Gtk.ToggleButton(label = Label_3)
        self.toggle3.connect('toggled', self.on_toggled3, 'toggle')
        self.toggle0.set_size_request(200, 0)
        #--------------------------------------

        #--------------------------------------
        # Lay out the buttons & display them
        #--------------------------------------
        grid = Gtk.Grid()
        grid.add(self.toggle0)
        grid.attach_next_to(self.toggle1, self.toggle0, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(self.toggle2, self.toggle1, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(self.toggle3, self.toggle2, Gtk.PositionType.BOTTOM, 1, 2)
        TheWindow.add(grid)

        TheWindow.show_all()
        #--------------------------------------
        print(">>> 2 <<<", S_Devices[0][2], S_Devices[1][2], S_Devices[2][2], S_Devices[3][2])

    #--------------------------------------
    # Another of the truly FUGLY parts...
    # There is probably a way to define a
    # single 'on_toggle()' & tell it which
    # device is being toggled.
    #
    # Of course, Life will be better
    # if/when I figure out how to handle
    # the "State" information returned from
    # the devices
    #--------------------------------------
    def on_toggled0(self, event, widget):
        state = self.toggle0.get_active()

        if state == True:
            self.label = self.toggle0.get_child()
            self.label.set_markup('<b>'+Device_0+' - ON </b>')  
            client.publish("cmnd/"+Device_0+"/"+Part_0, "on")
        else:
            self.toggle0.set_label(''+Device_0+' - OFF')
            client.publish("cmnd/"+Device_0+"/"+Part_0, "off")

    def on_toggled1(self, event, widget):
        state = self.toggle1.get_active()

        if state == True:
            self.label = self.toggle1.get_child()
            self.label.set_markup('<b>'+Device_1+' - ON </b>')  
            client.publish("cmnd/"+Device_1+"/"+Part_1, "on")
        else:
            self.toggle1.set_label(''+Device_1+' - OFF')
            client.publish("cmnd/"+Device_1+"/"+Part_1, "off")

    def on_toggled2(self, event, widget):
        state = self.toggle2.get_active()

        if state == True:
            self.label = self.toggle2.get_child()
            self.label.set_markup('<b>'+Device_2+' - ON </b>')  
            client.publish("cmnd/"+Device_2+"/"+Part_2, "on")
        else:
            self.toggle2.set_label(''+Device_2+' - OFF')
            client.publish("cmnd/"+Device_2+"/"+Part_2, "off")

    def on_toggled3(self, event, widget):
        state = self.toggle3.get_active()

        if state == True:
            self.label = self.toggle3.get_child()
            self.label.set_markup('<b>'+Device_3+' - ON </b>')  
            client.publish("cmnd/"+Device_3+"/"+Part_3, "on")
        else:
            self.toggle3.set_label(''+Device_3+' - OFF')
            client.publish("cmnd/"+Device_3+"/"+Part_3, "off")
    #--------------------------------------

    def main(self):
        Gtk.main()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

if __name__=='__main__':
    run = TOGGLE_WINDOW()
    client.connect(mqttBroker) 
    client.loop_start() #start the loop
    print(">>> 0 <<<", S_Devices[0][2], S_Devices[1][2], S_Devices[2][2], S_Devices[3][2])
    # run = TOGGLE_WINDOW()
    run.main()