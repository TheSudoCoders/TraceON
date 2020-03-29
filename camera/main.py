#! /usr/bin/env python

import cv2
import base64
import paho.mqtt.client as mqtt
import uuid
import json
import time
from   device_config import config
import ssl
import RPi.GPIO as GPIO
import datetime

LIMIT = 10
INTERVAL = 3 # 3 seconds cooldown
X = 1
sensor_pin = 17
def sensor_pin_read(): 
  return not GPIO.input(sensor_pin) # should follow some logic on GPIO pin

def on_connect(client, userdata, flags, rc):
  print ("Connected with result code:" + str(rc))

# this thing is required if we are receiving from MQTT broker
def on_message(client, userdate, msg):
  print (msg.topic, msg.payload)

if __name__=="__main__":
  print "********************\n", "*     Trace On     *\n", "********************"
  print "Start at", datetime.datetime.now()

  triggered = False

  # Initialize sensor
  GPIO.setmode(GPIO.BCM)
  sensor = GPIO.setup(sensor_pin, GPIO.IN)

  # open camera
  #  cap = cv2.VideoCapture(0)

  # prepare mqtt client
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message
  client.tls_set(ca_certs=config.ca_certs, certfile=config.certfile, keyfile=config.keyfile, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
  client.connect(config.broker, port=8883)

  while(True):
    # a trigger to send images to IoT
    if (triggered):
      # open camera
      cap = cv2.VideoCapture(0)

      image_id = uuid.uuid4().hex
      for i in range(0,LIMIT):
        # convert 10 frames to hex
        retval, image = cap.read()
        # cv2.imwrite("nikgay.jpg", image)
        jpg_as_text = base64.b64encode(cv2.imencode('.jpg', image)[1])
        # preparing load
        payload = {
                    "device_id": config.device_id,
                    "image_id" : str(image_id),
                    "payload" : jpg_as_text
                  }
        payload = json.dumps(payload)
        # print "payload", i, image_id
        client.publish(config.topic, payload, qos = 0, retain=False)
        time.sleep(2 * 0.1) # takes 10 images in a X second interval
      triggered = False
      cap.release()
      print "payload sent! Device UUID:", config.device_id, "    payload_id:", image_id
      time.sleep(INTERVAL) # cooldown before reading
    else:
        triggered = sensor_pin_read() # if true then goes up, if false stays here
