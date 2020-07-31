#!/usr/bin/python3

import csv
import os
import random

train_fh = open('train.txt','w')
test_fh = open('test.txt','w')


# work through the datafile and create train/test sets
fh = open('../birds.csv','r')
for i,datafile_line in enumerate(csv.reader(fh)):

    # skip the first line
    if i==0:
        continue

    # datafile format is:
    # id,path,x,y,box_h,box_w,h,w,label,dir,english,bird_group,isdir
    image_data = datafile_line
    filename,filepath,group = image_data[0],image_data[1],image_data[11]

    # pick a number between 1 and 10
    if random.randint(1,10) >= 8:
        train_fh.write("data/obj/" + str(filename) + ".jpg\n")
    else:
        test_fh.write("data/obj/" + str(filename) + ".jpg\n")

train_fh.close()
test_fh.close()

