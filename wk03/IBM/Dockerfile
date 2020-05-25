FROM python:3.7-alpine

WORKDIR /mnt/mybucket

RUN apk update
RUN apk upgrade
RUN apk add mosquitto
RUN apk add mosquitto-clients
RUN pip3 install paho-mqtt
