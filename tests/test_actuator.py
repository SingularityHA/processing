#!/usr/bin/python
"""
    SingularityHA Processing
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 - by Internet by Design Ltd
    :license: GPL v3, see LICENSE for more details.

"""

import mosquitto
import os
import json
import time
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/../../lib")
from config import config

serialdev = str(config.get("rfm_ninjablock", "serialdev"))
broker = str(config.get("mqtt", "host"))
port = int(config.get("mqtt", "port"))


def on_connect(rc):
    print "Connected"


def on_connect(rc):
    if rc == 0:
        #rc 0 successful connect
        print "Actuator test connected to MQTT"
    else:
        raise Exception


def on_publish(val):
    print "Published ", val


def cleanup():
    print "Ending and cleaning up"
    ser.close()
    mqttc.disconnect()


mypid = os.getpid()
client_uniq = "arduino_pub_" + str(mypid)
mqttc = mosquitto.Mosquitto(client_uniq)

mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.connect(broker, port, 60, True)

while mqttc.loop() == 0:
    mqttc.publish("actuators", json.dumps(["NBswitch", "DriveLight", "on"]))
    time.sleep(1)
    mqttc.publish("actuators", json.dumps(["NBswitch", "DriveLight", "off"]))
    break
    pass
