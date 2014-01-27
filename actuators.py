# SingularityHA
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
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/../lib")
from config import config
import logging

logger = logging.getLogger(__name__)

for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))):
                for dir in dirs:
                        if dir != "processing":
                                actuator_source = []
                                if os.path.isfile(os.path.join(root,dir,"actuators.py")):
                                        execfile(os.path.join(root,dir,"actuators.py"))
                                        actuator = actuator + actuator_source
                dirs[:] = []

broker = str(config.get("mqtt", "host"))
port = int(config.get("mqtt", "port"))

mqttc = mosquitto.Mosquitto("singularity-processing-actuators")

def on_connect(rc):
	logger.debug("ACTUARTORS Connected to MQTT")

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
		logger.info("Starting...")
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
