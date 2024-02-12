#!/usr/bin/env python

import pandas as pd 
import matplotlib.pyplot as plt
import json 
import os 
import sys

def find_min_max(x, y):
    assert(len(x) == len(y))

    x_min = float('inf')
    x_max = float('-inf')
    y_min = float('inf')
    y_max = float('-inf')

    for i in range(len(x)):
        if x[i] == y[i] == 0:
            continue 
        x_min = min(x_min, x[i])
        y_min = min(y_min, y[i])
        x_max = max(x_max, x[i])
        y_max = max(y_max, y[i])

    return x_min, y_min, x_max, y_max


def proc_frame(filepath):
    img_json = pd.read_json(filepath)
    kp = img_json.people[0]['pose_keypoints_2d']

    index = 0
    assert(len(kp) % 3 == 0)
    length = int(len(kp)/3)

    x = kp[0::3]
    y = kp[1::3]
    c = kp[2::3]
    assert(len(x) == len(y))

    x_min, y_min, x_max, y_max = find_min_max(x, y)
    x_range = x_max - x_min
    y_range = y_max - y_min
    alpha = y_range/x_range

    def scale(x_i, y_i):
        new_x = (x_i - x_min)/x_range
        new_y = alpha*(y_i - y_min)/y_range 
        return new_x, new_y  

    #print("x_range: ", x_range)
    #print("y_range: ", y_range)
    #print("alpha: ", alpha)

    #print(x_min, y_min, x_max, y_max)

    new_coords = []
    for i in range(len(x)):
        #print("Orig: ", x[i], y[i])
        if x[i] == y[i] == 0:
           nx, ny = 0, 0 
        else:
           nx, ny = scale(x[i], y[i])
        #print("Scaled: ", nx, ny)
        #print()
        new_coords.append(nx)
        new_coords.append(ny)

    # Commenting this for future lief, who may want to use this :..)
    '''
    for i in range(0, len(kp), 3):
        xv, yv = img_json.people[0]['pose_keypoints_2d'][i:i+2]
        print(xv, yv)
        xvs, yvs = scale(xv, yv)
        img_json.people[0]['pose_keypoints_2d'][i] = xvs
        img_json.people[0]['pose_keypoints_2d'][i + 1] = yvs

    return img_json
    '''
    return new_coords 

def proc_folder(folder):
    files = os.listdir(folder)
    new_folder = "normalised-" + folder
    os.mkdir(new_folder)
    for filename in files:
        new_coords = proc_frame(os.path.join(folder, filename))
        basename, ext = filename.split(".")
        new_filename = basename + "-normalised." + ext
        new_path = os.path.join(new_folder, new_filename)
        with open(new_path, 'w') as f:
            json.dump(new_coords, f)
        # pd.to_json(new_path, new_json)
        print("\tfile: ", filename, " complete!")

folders = ["0-ExtDerriereOnRight",
            "12-ExtSecondRight",
            "13-ExtSecondLeft",
            "1-ExtDerriereOnLeft",
            "3-EchappeSecond"]

for folder in folders:
    print("FOLDER: ", folder, ":")
    proc_folder(folder)

exit(1)
filename = "ALB0000_000000000214_keypoints.json"
filepath = os.path.join(folders[0], filename)
print(filepath)

for f in folders:
    print(f)


# some tests


for i in range(len(x)):
    sc = scale(x[i], y[i])
    print(sc if sc[1] > 1 else "")
