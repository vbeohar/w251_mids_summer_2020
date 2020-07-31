#!/usr/bin/python3

import csv
import os

# yolo file format
# <object-class> <x_center> <y_center> <width> <height>

# we could be slick about this, but what we really need is consistency, so:
obj_dict = {'blackbird':0, 'bluejay':1, 'cardinal':2, 'catbird':3, 'chickadee':4,
           'dove':5, 'goldfinch':6, 'grackle':7, 'grosbeak':8, 'oriole':9, 'robin':10,
           'sparrow':11 ,'thrasher':12, 'warbler':13 ,'woodpecker':14 ,'wren':15}

# lets work through the birds file to create an object file
fh = open('../birds.csv','r')
for i,datafile_line in enumerate(csv.reader(fh)):

    # skip the first line
    if i==0:
        continue

    # datafile format is:
    # id,path,x,y,box_h,box_w,h,w,label,dir,english,bird_group,isdir
    # id,path,x,y,box_w,box_h,h,w,label,dir,english,bird_group,isdir
    #image_data = datafile_line.split(',',)
    image_data = datafile_line
    filename,filepath,group = image_data[0],image_data[1],image_data[11]

    # first make sure that we have object mapping taken care of
    group = group.replace(' ','').lower()
    object_class = obj_dict[group]

    # now lets do centers (h=6, w=7)
    x_center = round((int(image_data[2]) + int(image_data[4])/2) / int(image_data[7]),6)
    y_center = round((int(image_data[3]) + int(image_data[5])/2) / int(image_data[6]),6)
    
    # now the height and width
    height = round(int(image_data[4]) / int(image_data[6]),6)
    width = round(int(image_data[5]) / int(image_data[7]),6)

    # print out the datafile
    out_string = str(object_class) + " " + str(x_center) + " " + str(y_center) + " " + str(width) + " " + str(height) + '\n'

    dest_filename = "/root/darknet/data/obj/" + filename + ".txt"
    fh2 = open(dest_filename,'w')
    try:
        fh2.write(out_string)
    except:
        print("failure to write: " + dest_filename)
    fh2.close()

    src_filename = "/root/tmp/" + filepath
    dest_filename = "/root/darknet/data/obj/" + filename + ".jpg"
    try:
        os.rename(src_filename,dest_filename)
    except:
        print("ERROR",src_filename,dest_filename)


