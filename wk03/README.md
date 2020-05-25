## <B> UC Berkeley, MIDS -  Summer 2020, w251 [ML @ edge/cloud]</B> (Vaibhav Beohar)


<B>Purpose of this assignment </B>: The objective of this homework is to build a lightweight IoT application pipeline with components running both on the edge (your Nvidia Jetson TX2) and the cloud (a VM in Softlayer). We also request that you pay attention to the architecture: write the application in a modular way, and such that it could be run on pretty much any low power edge device or hub (e.g. Raspberry Pi or Raspberry Pi Zero) and a cheap Cloud VM - or, indeed, another low power edge device connected to some kind of storage instead of a Cloud VM.

The overall goal of the assignment is to be able to capture faces in a video stream coming from the edge in real time, transmit them to the cloud in real time, and - for now, just save these faces in the cloud for long term storage.

[More info can be found here](https://github.com/MIDS-scaling-up/v2/tree/master/week03/hw)

Overall architecture of our application:
![](hw03.png)

###### Solution Steps:

On Jetson
-----------
On Jetson Tx2, we need to create the followoing primary containers :
- Docker container for messaging broker
- Docker container for messaging forwarder


Also note that we will be using `test_topic` as the name of message forwarder and subscriber topics on both Jetson and IBM-cloud. Please check the associated Python files for details.

##### Prepare Mosquitto Broker code on Jetson
- First step is to create a docker network and MQTT enabled broker that acts as intermediary between the message forwarder and remote host:
```
# Create a bridge:
docker network create --driver bridge hw03
# Create an alpine linux - based mosquitto container:
docker run --name mosquitto --network hw03 -p 1883:1883 -ti alpine sh
# we are inside the container now
# install mosquitto
apk update && apk add mosquitto
# run mosquitto
/usr/sbin/mosquitto
# Press Control-P Control-Q to disconnect from the container
```

##### Prepare Mosquitto Forwarder code on Jetson
- <B> Build container </B>: Using `Dockerfile`. The following `Dockerfile` is needed to build images for the forwarding container. This script loads Cuda and OpenCV libraries and creates a working directory `/home/midscode` on Jetson where the docker container scripts are loaded (should be on same network as above broker container, in this case `hw03`):
```
    # FROM cudabase-dev
    FROM w251/cuda:dev-tx2-4.3_b132

    ARG URL=http://169.44.201.108:7002/jetpacks/4.3

    RUN apt-get update && apt install -y git pkg-config wget build-essential cmake unzip

    WORKDIR /tmp
    # RUN rm *.deb

    RUN curl $URL/libopencv_3.3.1-2-g31ccdfe11_arm64.deb  -so libopencv_3.3.1-2-g31ccdfe11_arm64.deb
    RUN curl $URL/libopencv-dev_3.3.1-2-g31ccdfe11_arm64.deb -so libopencv-dev_3.3.1-2-g31ccdfe11_arm64.deb
    RUN curl $URL/libopencv-python_3.3.1-2-g31ccdfe11_arm64.deb -so libopencv-python_3.3.1-2-g31ccdfe11_arm64.deb

    RUN apt remove -y libopencv-calib3d-dev libopencv-core-dev

    RUN apt install -y  libtbb-dev libavcodec-dev libavformat-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk2.0-dev
    RUN apt install -y libswscale-dev libv4l-dev
    RUN dpkg -i *.deb

    RUN apt install -y libcanberra-gtk-module libcanberra-gtk3-module libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

    RUN apt install -y mosquitto python3 python3-pip python3-numpy python3-opencv
    RUN pip3 install paho-mqtt
    WORKDIR /home/midscode
```
- <B> Python script </B>  `img_capture_forwarder.py` that activates USB connected webcam, takes photos and then forwards them to the IBM cloud VSI on IP adddress (check the script for `test_topic` as the name of message forwarder and subscriber topics on both Jetson and IBM-cloud)
- `haarcascade_frontalface_default.xml` used to recognize faces
- <B> Run docker forwarder invoking commands and copy Python and XML files inside the container </B>. Following commands build Docker image, activate local USB camera on the Jetson, run the container in Bash shell mode and then copies the python and XML scripts inside the container (using the following commands):
```
  sudo docker build .
  sudo docker images
  xhost local:root  
  sudo docker run --name img_forwarder --network hw03 -it --device=/dev/video1:/dev/video1 -e DISPLAY=$DISPLAY --privileged --rm --env QT_X11_NO_MITSHM=1 <image_name> /bin/bash
  sudo docker exec -i img_forwarder sh -c 'cat > img_capture_forwarder.py' < /home/vebs/Documents/w251/wk03/img_capture_forwarder.py
  sudo docker exec -i img_forwarder sh -c 'cat > haarcascade_frontalface_default.xml' < /home/vebs/Documents/w251/wk03/haarcascade_frontalface_default.xml
```




On IBM Cloud
------------------------
On our IBM cloud VSI, we need to create the followoing primary containers.:
- Docker container for messaging broker
- Docker container for messaging subscriber (should be on same network as above broker container, in this case `hw03`)

In addition, we also need to set up our Amazon S3 bucket and mount it on our cloud VSI for storage of captured images.

Please note that the 2nd Docker container (subscriber) should be invoked with volume mount on `/mnt/mybucket` on the IBM VSI, which is our common directory where Amazon S3 bucket is mounted. Hence, when we start our Docker container, we will pass `-v` argument as such.

-  Before starting, make sure `/mnt/mybucket` is mounted to Amazon S3 by running following command (here `vebsbuck` is the name of S3 bucket):
```
    sudo s3fs vebsbuck /mnt/mybucket -o passwd_file=$HOME/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.direct.us-east.cloud-object-storage.appdomain.cloud
```
- Go into your working directory (in this case `/root/wk03` and ensure you have the following files present):
```
Dockerfile
msg_sub_save.py
```

##### Prepare Mosquitto Broker on IBM cloud (to accept incoming files)
-  <B>MQTT broker running on 1st container</B> - create your first Docker container, that acts as broker, running on a Docker network (also called `hw03`) that accepts incoming traffic and forwards the messages to the local topic:
```
# Create a bridge:
docker network create --driver bridge hw03
# Create an alpine linux - based mosquitto container:
docker run --name mosquitto --network hw03 -p 1883:1883 -ti alpine sh
# we are inside the container now
# install mosquitto
apk update && apk add mosquitto
# run mosquitto
/usr/sbin/mosquitto
# Press Control-P Control-Q to disconnect from the container
```

##### Prepare Mosquitto Subscriber [Python code] on IBM cloud (to accept incoming files)
-  <B>Build image using following Dockerfile</B>:
```
  FROM python:3.7-alpine

  WORKDIR /mnt/mybucket

  RUN apk update
  RUN apk upgrade
  RUN apk add mosquitto
  RUN apk add mosquitto-clients
  RUN pip3 install paho-mqtt
```
-  <B>MQTT subscriber running on 2nd container</B> - use folllowing commands in your home directory to invoke Docker container and copy files:
```
  docker build .
  docker images
  docker run --name python_img_receiver --network hw03 -it --privileged -v /mnt/mybucket:/mnt/mybucket <image_id>
  sudo docker exec -i python_img_receiver sh -c 'cat > msg_sub_save.py' < /root/wk03/msg_sub_save.py
```


- Follow links uploaded on S3 to check (here is an example of a sample uploaded image): [https://s3.us-east.cloud-object-storage.appdomain.cloud/vebsbuck/0.262784748079786.png](https://s3.us-east.cloud-object-storage.appdomain.cloud/vebsbuck/0.262784748079786.png)
