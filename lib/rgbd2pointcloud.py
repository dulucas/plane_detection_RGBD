import numpy as np
from lib.params_camera import config

### source code : https://svncvpr.in.tum.de/cvpr-ros-pkg/trunk/rgbd_benchmark/rgbd_benchmark_tools/src/rgbd_benchmark_tools/generate_pointcloud.py ###

"""
This script reads a registered pair of color and depth images and generates a
colored 3D point cloud.
"""

def rgbd2pointcloud(rgb, depth, debug_mode = False):
	if rgb.shape[:2] != depth.shape:
		raise Exception("Color and depth image do not have the same resolution.")
	points = []
	dict_depth_point = {}
	for v in range(rgb.shape[1]):
		for u in range(rgb.shape[0]):
			color = rgb[u,v]
			Z = depth[u,v] / config.scalingfactor
			if debug_mode:
				print('scaled depth : ', Z)
			if Z == 0: 
				continue
			X = (u - config.centerX) * Z / config.focal_length
			Y = (v - config.centerY) * Z / config.focal_length
			points.append([X, Y, Z])
			dict_depth_point[str([u, v, depth[u,v]])] = np.array([X, Y, Z, 1]).reshape((4,1))
	return points, dict_depth_point
