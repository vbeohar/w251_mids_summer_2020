#!/usr/bin/python3

import pandas as pd
import os
import sys

pd = pd.read_csv('birds.csv')

# first take care of the groupings
groups = pd.bird_group.unique()
groups = [x.lower() for x in groups]
groups = [x.replace(' ','') for x in groups]

# now iterate the rows in the csv and do some movement
fh = open('birds.csv','r')
for datafile_line in fh:
    image_data = datafile_line.split(',')
    filename,filepath,group = image_data[0],image_data[1],image_data[11]

    group = group.replace(' ','').lower()
    dest_filename = "/data01/nabirds_clean/" + group + "/" + filename + ".jpg"
    try:
        os.rename(filepath,dest_filename) 
    except:
        print("Error attempting to rename: {}".format(dest_filename))
        print(filepath)
        print(dest_filename)



