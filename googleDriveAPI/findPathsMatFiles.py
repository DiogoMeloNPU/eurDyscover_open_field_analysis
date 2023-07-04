import os

root = 'C:\\Users\\user\\Desktop\\Organized_data_JAS'

# list of all files from all mice (VideoProcessed)
file_list = []

for path, subdirs, files in os.walk(root):
    for file_name in files:
        if '.mat' in file_name:
            file_list.append((os.path.join(path, file_name)))