import os
import colorsys

import numpy as np
from keras import backend as K
from keras.models import load_model
from keras.layers import Input

from yolo4.model import yolo_eval, yolo4_body
from yolo4.utils import letterbox_image

from PIL import Image, ImageFont, ImageDraw
from timeit import default_timer as timer
import cv2

from decode_np import Decode

def detect_image(self, image, draw_image):
    pimage = self.process_image(np.copy(image))

    boxes, scores, classes = self.predict(pimage, image.shape)
    if boxes is not None and draw_image:
        self.draw(image, boxes, scores, classes)
    return image, boxes, scores, classes

def get_class(classes_path):
    classes_path = os.path.expanduser(classes_path)
    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names

def get_anchors(anchors_path):
    anchors_path = os.path.expanduser(anchors_path)
    with open(anchors_path) as f:
        anchors = f.readline()
    anchors = [float(x) for x in anchors.split(',')]
    return np.array(anchors).reshape(-1, 2)

if __name__ == '__main__':
    print('Please visit https://github.com/miemie2013/Keras-YOLOv4 for more complete model!')

    # model_path = 'ep073-loss11.905.h5'
    # anchors_path = 'model_data/yolo4_anchors.txt'
    # classes_path = 'model_data/voc_classes.txt'

    model_path = '../../model/yolo-obj_2000.h5'
    anchors_path = 'model_data/yolo4_anchors.txt'
    classes_path = '../../model/bird_classes.txt'

    class_names = get_class(classes_path)
    anchors = get_anchors(anchors_path)

    num_anchors = len(anchors)
    num_classes = len(class_names)

    model_image_size = (608, 608)

    # 分数阈值和nms_iou阈值
    conf_thresh = 0.2
    nms_thresh = 0.45

    yolo4_model = yolo4_body(Input(shape=model_image_size+(3,)), num_anchors//3, num_classes)

    model_path = os.path.expanduser(model_path)
    assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

    yolo4_model.load_weights(model_path)

    _decode = Decode(conf_thresh, nms_thresh, model_image_size, yolo4_model, class_names)


    ### test code #################
    ##################################
    # video_path = os.path.join("video", "birds.mp4")
    # camera = cv2.VideoCapture(video_path)
    # cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)

    # # Prepare for saving the detected video
    # sz = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
    #         int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # fourcc = cv2.VideoWriter_fourcc(*'mpeg')

    # vout = cv2.VideoWriter()
    # vout.open(os.path.join("videos", "res", video), fourcc, 20, sz, True)

    # while True:
    #     res, frame = camera.read()

    #     if not res:
    #         break

    #     image = detect_image(frame)
    #     cv2.imshow("detection", image)

    #     # Save the video frame by frame
    #     vout.write(image)

    #     if cv2.waitKey(110) & 0xff == 27:
    #         break

    # vout.release()
    # camera.release()

    

    ### test code #################
    ##################################

    while True:
        img = input('Input image filename:')
        try:
            image = cv2.imread(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            # image, boxes, scores, classes = _decode.detect_image(image, True)
            boxes, scores, classes = _decode.detect_video("birds.mp4")
            # _decode.detect_video("birds.mpeg")
            cv2.imshow('image', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    yolo4_model.close_session()