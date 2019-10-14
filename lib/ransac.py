import numpy as np
import random
from lib.params_camera import config

def ransac(pointcloud):
	count = 0
	best_plane_detected = []
	pointcloud = list(pointcloud)
	best_plane = None
	best_num_inliers = 0
	while count < config.num_iters_for_points:
		point_group = pointcloud # random.sample(pointcloud, config.num_groups)
		iters = 0
		while iters < config.num_iters_for_plane:
			num_inliers = 0
			random.shuffle(point_group)
			point_plane = point_group[:3]
			rest_point = point_group[3:]
			plane = estimate(point_plane)
			for point in rest_point:
				if is_inlier(point, plane, config.error_tolerated):
					num_inliers += 1
			if num_inliers > best_num_inliers:
				best_plane = plane
				best_num_inliers = num_inliers
				if num_inliers / config.num_groups > config.threhold_percentage:
					break
			iters += 1
		count += 1
	return best_plane, best_num_inliers / len(rest_point)

def solvequation(point_plane):
	point0, point1, point2 = point_plane[0], point_plane[1], point_plane[2]
	matrix_A = np.array([point0, point1, point2])
	matrix_A = matrix_A.reshape((3,3))
	#vector_b = np.zeros(3)
	plane_coeff = np.linalg.svd(matrix_A)[-1][-1, :]
	return plane_coeff

def estimate_inlier(point, plane):
	point = np.array(point).reshape((3,1))
	plane = np.array(plane).reshape((1,3))
	return np.dot(plane, point) < config.error_tolerated

def augment(xyzs):
	axyz = np.ones((len(xyzs), 4))
	axyz[:, :3] = xyzs
	return axyz

def is_inlier(xyz, coeffs, threshold):
	return np.abs(coeffs.dot(augment([xyz]).T)) < threshold

def estimate(xyzs):
	axyz = augment(xyzs[:3])
	return np.linalg.svd(axyz)[-1][-1, :]
