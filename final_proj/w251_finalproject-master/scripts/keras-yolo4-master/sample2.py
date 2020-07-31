# creating two lists to store predicted and actual tags
predict = []
actual = []

video_file = 'input_filename'
cap = cv2.VideoCapture(video_file)
  frameRate = cap.get(5) 

  while(cap.isOpened()):
    frameId = cap.get(1)
    ret, frame = cap.read()
    if (ret != True):
      break
    if (frameId % math.floor(frameRate) == 0):
      # storing the frames of this particular video in temp folder
      filename ='temp/' + "_frame%d.jpg" % count;count+=1
      cv2.imwrite(filename, frame)
cap.release()
    
# reading all the frames from temp folder
images = glob("temp/*.jpg")
    
prediction_images = []
for i in range(len(images)):
  img = image.load_img(images[i], target_size=(224,224,3))
  img = image.img_to_array(img)
  img = img/255
  prediction_images.append(img)
        
  # converting all the frames for a test video into numpy array
  prediction_images = np.array(prediction_images)
  # extracting features using pre-trained model
  prediction_images = base_model.predict(prediction_images)
  # converting features in one dimensional array
  prediction_images = prediction_images.reshape(prediction_images.shape[0], 7*7*512)
  # predicting tags for each array
  prediction = model.predict_classes(prediction_images)
  # appending the mode of predictions in predict list to assign the tag to the video
  predict.append(y.columns.values[s.mode(prediction)[0][0]])
  # appending the actual tag of the video
  actual.append(videoFile.split('/')[1].split('_')[1])
