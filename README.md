An attempt at creating a desktop application to replace a Node-Red dashboard group.

Just because putting a small control set on the desktop really shouldn't require firing up yet another web browser window.

# Yes, I know this is the fugliest code ever seen.

Just as a starting point, I've never been much good with UI programming.

To make it worse, I have absolutely no experience with Python.

# OTOH...

It seems to work.

It's hard coded to work on MY network with MY SiniLinks... (Tho, now the "hard coding" is almost entirely in easily found variables now.)

(My SiniLinks run [firmware](https://github.com/cdntinker/WIP-IoT-Smart_Switch) that acts much like TasmOTA as far as MQTT goes.)

meh...

# To Be Done
At this moment, the states of the SiniLinks, as shown on the buttons, are NOT determined from the devices themselves.

At startup, they all show "wtf" by default.

The first time a button is pressed, an ON command is sent.

This is not optimal...
