#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation

# This shows an example of using the publish.single helper function.

import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import serial #Import Serial Library
import json
import time
 
arduinoSerialData = serial.Serial('com5',9600) #Create Serial port object called arduinoSerialData
 
 
while True:
    if (arduinoSerialData.inWaiting()>0):
        ts = time.time()
        myData = arduinoSerialData.readline()
        myData = myData.decode("utf-8")
        myData = myData.rstrip()
        temp = myData[0:3]
        temp = float(temp)
        hum = myData[4:8]
        direction = myData[8]
        if direction == "0":
            direction = "SE"
        elif direction == "1":
            direction = "SW"
        myData = json.dumps( {'latitude':35.6133125,'longitude': -83.4990472,'airHumidity': hum, 'airTemperature': temp, 'windDirection': direction, 'timestamp': ts} )
        print (myData)
        #publish.single("weatherbot-accmty2018", myData, hostname="test.mosquitto.org")

'''def print_msg(client, userdata, message):
    print("%s : %s" % (message.topic, message.payload))

subscribe.callback(print_msg, "topic1", hostname="test.mosquitto.org")
'''

