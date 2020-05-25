#!/usr/bin/python3
import cv2
import os
import paho.mqtt.client as mqtt

local_sub_ip = input('\n enter remote subscriber id address <return> ==>  ')

LOCAL_MQTT_HOST= local_sub_ip
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="test_topic"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client,userdata, msg):
  try:
    print("message received!")
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

cam = cv2.VideoCapture(1)
cam.set(3, 640)
cam.set(4, 480)

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
face_id = input('\n enter user id end press <return> ==>  ')
print("\n [INFO] Initializing face capture. Look the camera and wait ...")
count = 0
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if (ret == True):
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        print("[INFO] Found {0} Faces.".format(len(faces)))
        for (x,y,w,h) in faces:
            face_trimmed = gray[y:y+h,x:x+w]
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1
            # Save the captured image into the datasets folder
            rc, png = cv2.imencode('.png', face_trimmed)
            msg = png.tobytes()
            try:
                print("publishing images")
                local_mqttclient.publish(LOCAL_MQTT_TOPIC, payload=msg, qos=0, retain=False)
            except:
                print("error, unable to write to mosquitto")
        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 30: # Take 30 face sample and stop video
             break
    else:
        print("frame returned false")

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
