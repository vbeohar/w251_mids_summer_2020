import sys
import time
import numpy as np
import tensorflow as tf
import cv2

import os
import paho.mqtt.client as mqtt

from utils import label_map_util
from utils import visualization_utils_color as vis_util

LOCAL_MQTT_HOST= '169.55.190.195'
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

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = './model/frozen_inference_graph_face.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = './protos/face_label_map.pbtxt'

NUM_CLASSES = 2

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

class TensoflowFaceDector(object):
  def __init__(self, PATH_TO_CKPT):
      """Tensorflow detector
      """

      self.detection_graph = tf.Graph()
      with self.detection_graph.as_default():
          od_graph_def = tf.compat.v1.GraphDef()
          with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
              serialized_graph = fid.read()
              od_graph_def.ParseFromString(serialized_graph)
              tf.import_graph_def(od_graph_def, name='')


      with self.detection_graph.as_default():
          config = tf.compat.v1.ConfigProto()
          config.gpu_options.allow_growth = True
          self.sess = tf.compat.v1.Session(graph=self.detection_graph, config=config)
          self.windowNotSet = True


  def run(self, image):
      """image: bgr image
      return (boxes, scores, classes, num_detections)
      """

      #image_np = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

      # the array based representation of the image will be used later in order to prepare the
      # result image with boxes and labels on it.
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      #image_np_expanded = np.expand_dims(image_np, axis=0)
      print(image.shape)
      image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
      # Each box represents a part of the image where a particular object was detected.
      boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
      # Each score represent how level of confidence for each of the objects.
      # Score is shown on the result image, together with the class label.
      scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
      classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
      # Actual detection.
      start_time = time.time()
      (boxes, scores, classes, num_detections) = self.sess.run(
          [boxes, scores, classes, num_detections],
          feed_dict={image_tensor: image})
      elapsed_time = time.time() - start_time
      print('inference time cost: {}'.format(elapsed_time))

      return (boxes, scores, classes, num_detections)


if __name__ == "__main__":
  import sys
  if len(sys.argv) != 2:
      print ("usage:%s (cameraID | filename) Detect faces in the video example:%s 0"%(sys.argv[0], sys.argv[0]))
      exit(1)

  try:
    camID = int(sys.argv[1])
  except:
    camID = sys.argv[1]

  tDetector = TensoflowFaceDector(PATH_TO_CKPT)

  cap = cv2.VideoCapture(camID)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
  cap.set(cv2.CAP_PROP_FPS, 12)

  windowNotSet = True
  while True:
      ret, image = cap.read()
      # We don't use the color information, so might as well save space
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      if ret == 0:
          break

      if ret == True:
          [h, w] = image.shape[:2]
          print (h, w)
          image = cv2.flip(image, 1)
          img = np.array(image).reshape(1,h,w,3)

          (boxes, scores, classes, num_detections) = tDetector.run(img)

          vis_util.visualize_boxes_and_labels_on_image_array(
              image,
              np.squeeze(boxes),
              np.squeeze(classes).astype(np.int32),
              np.squeeze(scores),
              category_index,
              use_normalized_coordinates=True,
              line_thickness=4)

          if windowNotSet is True:
              cv2.namedWindow("tensorflow based (%d, %d)" % (544, 288), cv2.WINDOW_NORMAL)
              windowNotSet = False

          # Save the captured image into the datasets folder
          rc, png = cv2.imencode('.png', image)
          msg = png.tobytes()
          try:
              print("publishing images")
              # gray = cv2.rectangle(gray, (0,0), (w,h), (255,0,0), 2)
              local_mqttclient.publish(LOCAL_MQTT_TOPIC, payload=msg, qos=0, retain=False)
          except:
              print("error, unable to write to mosquitto")

          cv2.imshow("tensorflow based (%d, %d)" % (w, h), image)
          k = cv2.waitKey(1) & 0xff
          if k == ord('q') or k == 27:
              break

  cap.release()
