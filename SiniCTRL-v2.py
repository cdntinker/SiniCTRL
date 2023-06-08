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
        client.subscribe([
            ("stat/"+Device_0+"/"+Part_0, 0),
            ("stat/"+Device_1+"/"+Part_1, 0),
            ("stat/"+Device_2+"/"+Part_2, 0),
            ("stat/"+Device_3+"/"+Part_3, 0),
            ])
        print('Subscribed to:\n\t{:s}\n\t{:s}\n\t{:s}\n\t{:s}'.format(
            Device_0+" - "+Part_0, 
            Device_1+" - "+Part_1, 
            Device_2+" - "+Part_2, 
            Device_3+" - "+Part_3
            ))
        ######################################################
        client.publish("cmnd/"+Device_0+"/"+"Status", "Power")
        client.publish("cmnd/"+Device_1+"/"+"Status", "Power")
        client.publish("cmnd/"+Device_2+"/"+"Status", "Power")
        client.publish("cmnd/"+Device_3+"/"+"Status", "Power")
        ######################################################

        #--------------------------------------
    else:
        print("Bad connection Returned code=",rc)

def on_message(client, userdata, message):
    #--------------------------------------
    # Yet ANOTHER truly FUGLY part...
    #--------------------------------------

    global State_0
    global State_1
    global State_2
    global State_3

    print("  topic:", message.topic)
    print("message:", str(message.payload.decode("utf-8")))

# These work for my firmware... Not so much for tasmota as it responds
# with a full JSON payload
# Might have to work on that once it's doing what I want for these devices
    if(message.topic == "stat/"+Device_0+"/"+Part_0):
        State_0 = str(message.payload.decode("utf-8"))
    if(message.topic == "stat/"+Device_1+"/"+Part_1):
        State_1 = str(message.payload.decode("utf-8"))
    if(message.topic == "stat/"+Device_2+"/"+Part_2):
        State_2 = str(message.payload.decode("utf-8"))
    if(message.topic == "stat/"+Device_3+"/"+Part_3):
        State_3 = str(message.payload.decode("utf-8"))

    # print('States:\n\t{:s}\n\t{:s}\n\t{:s}\n\t{:s}'.format(
    #     Device_0+" - "+State_0, 
    #     Device_1+" - "+State_1, 
    #     Device_2+" - "+State_2, 
    #     Device_3+" - "+State_3
    #     ))
    #--------------------------------------

client = mqtt.Client(client_id)
client.will_set(lwt_topic, payload="(I B ded)")

client.on_connect=on_connect    #bind call back function
client.on_message=on_message    #attach function to callback

#------------------------------------------------------------------------------
# The Window!
#------------------------------------------------------------------------------

# class TOGGLE_WINDOW:

def destroy(self, widget, data=None):
    print('destroy event occurred (i.e.: Window was closed...)')
    Gtk.main_quit()

    #--------------------------------------
    # Build the window
    #--------------------------------------

class ourwindow(Gtk.Window):

    ######################################################
    def get_states():
    # So...
    # How do I get it to run this so I have responses to those "Status" commands?
    # hhhmmm...
        # global State_0
        # global State_1
        # global State_2
        # global State_3
        client.publish("cmnd/"+Device_0+"/"+"Status", "Power")
        client.publish("cmnd/"+Device_1+"/"+"Status", "Power")
        client.publish("cmnd/"+Device_2+"/"+"Status", "Power")
        client.publish("cmnd/"+Device_3+"/"+"Status", "Power")
        # print(">>> STATES:", State_0, State_1, State_2, State_3)

        Label_0 = Device_0+' - '+State_0
        Label_1 = Device_1+' - '+State_1
        Label_2 = Device_2+' - '+State_2
        Label_3 = Device_3+' - '+State_3

        print(">>> STATES:", Label_0, Label_1, Label_2, Label_3)
    ######################################################

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
    def on_toggled0(self, event):
        state = Gtk.Window.toggle0.get_active()

        if state == True:
            self.label = Gtk.Window.toggle0.get_child()
            self.label.set_markup('<b>'+Device_0+' - ON </b>')  
            client.publish("cmnd/"+Device_0+"/"+Part_0, "on")
        else:
            Gtk.Window.toggle0.set_label(''+Device_0+' - OFF')
            client.publish("cmnd/"+Device_0+"/"+Part_0, "off")

    def on_toggled1(self, event):
        state = Gtk.Window.toggle1.get_active()

        if state == True:
            self.label = Gtk.Window.toggle1.get_child()
            self.label.set_markup('<b>'+Device_1+' - ON </b>')  
            client.publish("cmnd/"+Device_1+"/"+Part_1, "on")
        else:
            Gtk.Window.toggle1.set_label(''+Device_1+' - OFF')
            client.publish("cmnd/"+Device_1+"/"+Part_1, "off")

    def on_toggled2(self, event):
        state = Gtk.Window.toggle2.get_active()

        if state == True:
            self.label = Gtk.Window.toggle2.get_child()
            self.label.set_markup('<b>'+Device_2+' - ON </b>')  
            client.publish("cmnd/"+Device_2+"/"+Part_2, "on")
        else:
            Gtk.Window.toggle2.set_label(''+Device_2+' - OFF')
            client.publish("cmnd/"+Device_2+"/"+Part_2, "off")

    def on_toggled3(self, event):
        state = Gtk.Window.toggle3.get_active()

        if state == True:
            self.label = Gtk.Window.toggle3.get_child()
            self.label.set_markup('<b>'+Device_3+' - ON </b>')  
            client.publish("cmnd/"+Device_3+"/"+Part_3, "on")
        else:
            Gtk.Window.toggle3.set_label(''+Device_3+' - OFF')
            client.publish("cmnd/"+Device_3+"/"+Part_3, "off")
    #--------------------------------------

    TheWindow = Gtk.Window()
    TheWindow.set_position(Gtk.WindowPosition.CENTER)
    TheWindow.set_title(WindowTitle)
    # TheWindow.connect('destroy', Gtk.Window.destroy)

    #--------------------------------------
    # One of the truly FUGLY parts...
    # Should figure out how to turn it into
    # a loop.  Maybe build up an array or
    # structure to define the devices
    #--------------------------------------
    Gtk.Window.toggle0 = Gtk.ToggleButton(label = Device_0+' - '+State_0)
    Gtk.Window.toggle0.connect('toggled', on_toggled0, 'toggle')
    Gtk.Window.toggle0.set_size_request(200, 0)

    Gtk.Window.toggle1 = Gtk.ToggleButton(label = Device_1+' - '+State_1)
    Gtk.Window.toggle1.connect('toggled', on_toggled1, 'toggle')
    Gtk.Window.toggle0.set_size_request(200, 0)

    Gtk.Window.toggle2 = Gtk.ToggleButton(label = Device_2+' - '+State_2)
    Gtk.Window.toggle2.connect('toggled', on_toggled2, 'toggle')
    Gtk.Window.toggle0.set_size_request(200, 0)

    Gtk.Window.toggle3 = Gtk.ToggleButton(label = Device_3+' - '+State_3)
    Gtk.Window.toggle3.connect('toggled', on_toggled3, 'toggle')
    Gtk.Window.toggle0.set_size_request(200, 0)
    #--------------------------------------

    #--------------------------------------
    # Lay out the buttons & display them
    #--------------------------------------
    grid = Gtk.Grid()
    grid.add(Gtk.Window.toggle0)
    grid.attach_next_to(Gtk.Window.toggle1, Gtk.Window.toggle0, Gtk.PositionType.BOTTOM, 1, 2)
    grid.attach_next_to(Gtk.Window.toggle2, Gtk.Window.toggle1, Gtk.PositionType.BOTTOM, 1, 2)
    grid.attach_next_to(Gtk.Window.toggle3, Gtk.Window.toggle2, Gtk.PositionType.BOTTOM, 1, 2)
    TheWindow.add(grid)

    TheWindow.connect('destroy', Gtk.Window.destroy)
    TheWindow.show_all()
    #--------------------------------------

    def main(TheWindow):
        Gtk.main()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

if __name__=='__main__':
    client.connect(mqttBroker) 
    client.loop_start() #start the loop
    # window = ourwindow()
    # window.connect("delete-event", Gtk.main_quit)
    # window.show_all()

    # run = ourwindow()
    # run.main()

Gtk.main()
