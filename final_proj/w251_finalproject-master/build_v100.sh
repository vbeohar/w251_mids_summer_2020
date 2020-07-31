#!/bin/sh

SSHKEY=1811846
DATACENTER=dal10
MACHINE_TYPE=AC2_8X60X100
IMAGE_ID=2263543
HOSTNAME=fp-v100
DOMAIN=n-a.cloud

# AC2 is a V100

# this is the machine for final project birdhouse
ibmcloud sl vs create --datacenter=$DATACENTER --hostname=$HOSTNAME --domain=$DOMAIN --image=$IMAGE_ID --billing=hourly  --network 1000 --key=$SSHKEY --flavor $MACHINE_TYPE --san

