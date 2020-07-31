#!/usr/bin/python3

import pandas as pd
import os
import sys

pd = pd.read_csv('birds.csv')

groups = pd.bird_group.unique()
groups = [x.lower() for x in groups]
groups = [x.replace(' ','') for x in groups]

print(groups)
for group in groups:
    path = "/data01/nabirds_clean/" + group
    os.mkdir(path)
