"""
    SingularityHA Processing Module
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 - by Internet by Design Ltd
    :license: GPL v3, see LICENSE for more details.

"""

import mosquitto
import json
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/../lib")
from config import config
import logging

logger = logging.getLogger(__name__)

actuator = {}
actuator_source = {}
for filename in os.listdir(os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/actuatorfiles/"):
    if filename != "README":
        execfile(
            os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + "/actuatorfiles/", filename))
        actuator = dict(actuator.items() + actuator_source.items())

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
