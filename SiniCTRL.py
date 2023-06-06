#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import paho.mqtt.client as mqtt 

#------------------------------------------------------------------------------
# The Window!
#------------------------------------------------------------------------------

class TOGGLE_WINDOW:

    def delete_event(self, widget, event, data=None):
        print('delete event occurred')
        return False

    def destroy(self, widget, data=None):
        Gtk.main_quit()

    #--------------------------------------
    # Build the window
    #--------------------------------------
    def __init__(self):
        TheWindow = Gtk.Window()
        TheWindow.set_position(Gtk.WindowPosition.CENTER)
        TheWindow.set_title('SiniLink CTRLs')
        TheWindow.connect('delete_event', self.delete_event)
        TheWindow.connect('destroy', self.destroy)

        #--------------------------------------
        # One of the truly FUGLY parts...
        # Should figure out how to turn it into
        # a loop.  Maybe build up a set of
        # variables to define the devices
        #--------------------------------------
        self.toggle0 = Gtk.ToggleButton(label = 'SiniLink 0 - wtf')
        self.toggle0.connect('toggled', self.on_toggled0, 'toggle')
        self.toggle0.set_size_request(200, 0)

        self.toggle1 = Gtk.ToggleButton(label = 'SiniLink 1 - wtf')
        self.toggle1.connect('toggled', self.on_toggled1, 'toggle')
        self.toggle0.set_size_request(300, 0)

        self.toggle2 = Gtk.ToggleButton(label = 'SiniLink 2 - wtf')
        self.toggle2.connect('toggled', self.on_toggled2, 'toggle')
        self.toggle0.set_size_request(200, 0)

        self.toggle3 = Gtk.ToggleButton(label = 'SiniLink 3 - wtf')
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

    #--------------------------------------
    # Another of the truly FUGLY parts...
    # There is probably a way to define a
    # single 'on_toggle()' & tell it which
    # device is being toggled.
    #--------------------------------------
    def on_toggled0(self, event, widget):
        state = self.toggle0.get_active()

        if state == True:
            self.label = self.toggle0.get_child()
            self.label.set_markup('<b>SiniLink 0 - ON </b>')  
            client.publish("cmnd/Sinilink_0/Power", "on")
        else:
            self.toggle0.set_label('SiniLink 0 - OFF')
            client.publish("cmnd/Sinilink_0/Power", "off")

    def on_toggled1(self, event, widget):
        state = self.toggle1.get_active()

        if state == True:
            self.label = self.toggle1.get_child()
            self.label.set_markup('<b>SiniLink 1 - ON </b>')  
            client.publish("cmnd/Sinilink_1/Power", "on")
            print("Sent a ON command via MQTT to Sinilink_1")
        else:
            self.toggle1.set_label('SiniLink 1 - OFF')
            client.publish("cmnd/Sinilink_1/Power", "off")
            print("Sent a OFF command via MQTT to Sinilink_1")

    def on_toggled2(self, event, widget):
        state = self.toggle2.get_active()

        if state == True:
            self.label = self.toggle2.get_child()
            self.label.set_markup('<b>SiniLink 2 - ON </b>')  
            client.publish("cmnd/Sinilink_2/Power", "on")
        else:
            self.toggle2.set_label('SiniLink 2 - OFF')
            client.publish("cmnd/Sinilink_2/Power", "off")

    def on_toggled3(self, event, widget):
        state = self.toggle3.get_active()

        if state == True:
            self.label = self.toggle3.get_child()
            self.label.set_markup('<b>SiniLink 3 - ON </b>')  
            client.publish("cmnd/Sinilink_3/Power", "on")
        else:
            self.toggle3.set_label('SiniLink 3 - OFF')
            client.publish("cmnd/Sinilink_3/Power", "off")
    #--------------------------------------

    def main(self):
        Gtk.main()

#------------------------------------------------------------------------------
# MQTT Stuffz
#------------------------------------------------------------------------------

mqttBroker ="Skynet"                            # Specific to MY network

client = mqtt.Client("SiniLink_Controls2")      # This needs to be randomized to some extent...
client.connect(mqttBroker) 

#--------------------------------------
# Specific to MY network
# These are MY SiniLink USB switches
#--------------------------------------
client.subscribe("stat/Sinilink_0/Power")
print("Subscribed: stat/Sinilink_0/Power")

client.subscribe("stat/Sinilink_1/Power00")
print("Subscribed: stat/Sinilink_1/Power00")

client.subscribe("stat/Sinilink_2/Power")
print("Subscribed: stat/Sinilink_2/Power")

client.subscribe("stat/Sinilink_3/Power")
print("Subscribed: stat/Sinilink_3/Power")
#--------------------------------------

def on_message(client, userdata, message):
    #--------------------------------------
    # Yet ANOTHER truly FUGLY part...
    #--------------------------------------
    global State_0, State_1, State_2, State_3

    print("  topic:", message.topic)
    print("message:", str(message.payload.decode("utf-8")))

    if(message.topic == "stat/Sinilink_0/Power"):
        State_0 = str(message.payload.decode("utf-8"))
        print("MoFo! 0 " + State_0)
    if(message.topic == "stat/Sinilink_1/Power00"):
        State_1 = str(message.payload.decode("utf-8"))
        print("MoFo! 1 " + State_1)
    if(message.topic == "stat/Sinilink_2/Power"):
        State_2 = str(message.payload.decode("utf-8"))
        print("MoFo! 2 " + State_2)
    if(message.topic == "stat/Sinilink_3/Power"):
        State_3 = str(message.payload.decode("utf-8"))
        print("MoFo! 3 " + State_3)
    #--------------------------------------

client.on_message=on_message        #attach function to callback

client.loop_start() #start the loop

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

if __name__=='__main__':
    run = TOGGLE_WINDOW()
    run.main()