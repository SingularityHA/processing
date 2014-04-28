"""
    SingularityHA Processing
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 - by Internet by Design Ltd
    :license: GPL v3, see LICENSE for more details.

"""
import mosquitto
import json
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/../lib")
from config import config
import logging

logger = logging.getLogger("processing.sensors")

broker = str(config.get("mqtt", "host"))
port = int(config.get("mqtt", "port"))

mqttc = mosquitto.Mosquitto("singularity-processing-sensors")



def on_message(msg):
    inbound = json.loads(msg.payload)
    device = inbound[0]

    try:
        content = inbound[1]
    except IndexError:
        pass

    """ Do nothing because we don't have rules yet """
    print str(device)

    logging.debug(str(device))
    try:
        logging.debug(str(content))
    except:
        pass

def main():
    try:

        mqttc.on_message = on_message

        mqttc.connect(broker, port, 60, False)

        mqttc.subscribe("sensors", 0)

        while mqttc.loop() == 0:
            pass
    except KeyboardInterrupt:
        pass
