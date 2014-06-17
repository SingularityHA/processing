#!/usr/bin/env python
"""
    SingularityHA Processing
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 - by Internet by Design Ltd
    :license: GPL v3, see LICENSE for more details.

"""
import socket
import requests
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + "/../lib")
from config import config
import urllib2

root = config.get("general", "path")

r = json.loads(requests.get("http://" + config.get("general", "confighost") + "/api/v1/module_actuator/").text)

modules = {}
for module in r['objects']:
    if len(str(module['actuatorfile'])) > 7:
        response = urllib2.urlopen(module['actuatorfile'])
        html = response.read()
        target = open(os.path.dirname(os.path.realpath(__file__)) + "/actuatorfiles/" + module['name'] + ".py", 'w')
        target.write(html)
        target.close

