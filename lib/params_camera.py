import numpy as np
import cv2
from easydict import EasyDict as edict

C = edict()
config = C
C.user = 'Robot master'

# Params of camera
#C.intrinsic_parameters = [[1,0,0],[0,1,0],[0,0,1]]
#C.extrinsic_parameters = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]).reshape((4,4))
#C.extrinsic_parameters = np.array([[ 0.9985719 ,  0.00921411, -0.05262385,  0.01507933], [ 0.04437823,  0.40535598,  0.9130811 , -0.77583786], [ 0.02974462, -0.91411248,  0.40436819,  0.38050523], [0., 0., 0., 1.]]).reshape((4,4))
#np.array([[1,0,0,1],[0,1,0,1],[0,0,1,1],[1,1,1,1]]).reshape((4,4))
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
