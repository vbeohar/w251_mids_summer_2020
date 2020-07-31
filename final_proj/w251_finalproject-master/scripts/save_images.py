import os
import glob
os.system
import PIL
import PIL.Image as Image

# code from @mhusseinsh on gihub

d = 0
test_Path = r'\data\darknet_local\obj\data
with open((test_Path + '.txt'),'r') as fobj:
for line in fobj:
image_List = [[num for num in line.split()] for line in fobj]
for images in image_List:
commands = ['darknet.exe detector test data/obj.data yolo-obj_test.cfg backup/yolo-obj_4900.weights -dont_show', images[0]]
os.system(' '.join(commands))
predicted_image = Image.open("E:/ANPR/darknet/build/darknet/x64/predictions.jpg")
output = "E:/ANPR/darknet/build/darknet/x64/data/predictedimages/predicted_image%d.jpg"%d
predicted_image.save(output)
d+=1



