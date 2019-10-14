import numpy as np
import cv2
from easydict import EasyDict as edict

C = edict()
config = C
C.user = 'Robot master'

# Params of camera
C.focal_length = 500
C.centerX = 240
C.centerY = 320
C.scalingfactor = 1000

# File path of the images
C.target_dir = 'results/'
C.source_dir = 'XXX'

# Params for Ransac
C.num_iters_for_plane = 1 # number of times for the 3 points selection to define the plane
C.num_iters_for_points = 50 # number of times for random selection of points on the plane
C.error_tolerated = 2e-4
C.num_groups = 300 # number of selected groups for every iteration
C.threhold_percentage = 0.6 # threhold of percentage to admit a plane
C.threhold_depth = 3
C.threhold_mesh = 1000
C.kmeans_clusters = 5
