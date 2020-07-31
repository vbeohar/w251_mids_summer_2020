import os

fh = open('test.txt','r')

for filename in fh:
    filename = "/data01/darknet/" + filename.rstrip()
    if not os.path.exists(filename):
        print(filename)
