import csv
import numpy as np
from lib.params_camera import config

def csv2depth(name):
        result = []
        with open(name, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                result.append(row)
        result = np.array(result, dtype = np.float64)
        result[result > config.threhold_depth] = 0
        return result
