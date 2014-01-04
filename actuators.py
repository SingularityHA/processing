# Singularity
# Copyright (C) 2014 Internet by Design Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import mosquitto
import json
import time

broker = "127.0.0.1"
port = 1883

mqttc = mosquitto.Mosquitto("singularity-processing-actuators")

def on_connect(rc):
	print "ACTUARTORS Connected to MQTT"

#runs when a MQTT message arrives
def on_message(msg):
	#unpack json payload
	inbound = json.loads(msg.payload)
	
	#this is the device we are working with...
	cat = inbound[0]
	dev = inbound[1]
	#....and what we want to do with it
	intent = inbound[2]
	#some things need extra info
	data = None
	try:
		data = inbound[3]
	except IndexError:
		pass
	#use the lookup table to run the command for the device
	actuator[cat](dev, intent, data)

def main():

	try:	
		print "actuators"
		#start up the MQTT connection
		mqttc.on_message = on_message
		mqttc.on_connect = on_connect
		mqttc.connect(broker, port, 60, False)
		mqttc.subscribe("actuators", 0)

		#infinite loop until the MQTT connection dies
		while mqttc.loop() == 0:
			pass
	except KeyboardInterrupt:
		pass
