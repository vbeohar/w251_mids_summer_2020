# keras-yolo4

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

# 请使用更完善的版本:

# [https://github.com/miemie2013/Keras-YOLOv4](https://github.com/miemie2013/Keras-YOLOv4)

# Please visit here for more complete model:

# [https://github.com/miemie2013/Keras-YOLOv4](https://github.com/miemie2013/Keras-YOLOv4)

## <U> Dependencies </U>
* Tensorflow GPU 1.14
* Keras 2.3.1
* opencv-python 4.2.0
* imutils 0.5.3
* numpy 1.18.2
* sklearn

check more info here https://pythonawesome.com/deep-sort-and-yolo-v4-for-people-tracking-and-detection-with-tensorflow-backend/


## Introduction

A Keras implementation of YOLOv4 (Tensorflow backend) inspired by [https://github.com/AlexeyAB/darknet](https://github.com/AlexeyAB/darknet).

Frame code from [https://github.com/qqwweee/keras-yolo3](https://github.com/qqwweee/keras-yolo3).

![](yolo4.png)

---

## Quick Start

1. Download YOLOv4 weights from [yolov4.weights](https://drive.google.com/open?id=1cewMfusmPjYWbrnuJRuKhPMwRe_b9PaT).
2. Convert the Darknet YOLOv4 model to a Keras model.
3. Run YOLOv4 detection.

```
python convert.py
```

Running convert.py will get keras yolov4 weight file yolo4_weight.h5.


### Usage

Inference

```
python test.py
```
---

### Todo

Debug train code with CIoU loss. Loss code from [https://github.com/david8862/keras-YOLOv3-model-set](https://github.com/david8862/keras-YOLOv3-model-set).
