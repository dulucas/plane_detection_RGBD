import csv
import numpy as np
import cv2
from lib.params_camera import config

def csv2depth(name):
        result = []
        with open(name, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                result.append(row)
        result = np.array(result, dtype = np.float64)
        result[result > config.threhold_depth] = 0
        #depth = result / result.max() * 255
        #depth = np.array(depth, dtype = np.uint8)
        #cv2.imwrite('depth.png', depth)
        return result
