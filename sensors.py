
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

mqttc = mosquitto.Mosquitto("singularity-processing-sensors")

def on_connect(rc):
	print "SENSORS Connected to MQTT"

def on_message(msg):
	inbound = json.loads(msg.payload)
	medium = inbound[0]
	content = inbound[1]

	if str(medium) == "433mhz":
		print str(content)
		sensors[str(content)]()
	else:
		print "Medium " + medium + " not implemented!"


def main():
	try:

		mqttc.on_message = on_message
		mqttc.on_connect = on_connect
	
		mqttc.connect(broker, port, 60, False)

		mqttc.subscribe("sensors", 0)

		while mqttc.loop() == 0:
			pass
	except KeyboardInterrupt:
		pass
