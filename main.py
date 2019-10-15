import numpy as np
import argparse
import pickle as pkl
from PIL import Image
import matplotlib.pyplot as plt
import random
import cv2

from lib.rgbd2pointcloud import rgbd2pointcloud
from lib.ransac import ransac
from lib.ransac import is_inlier
from lib.csv2depth import csv2depth
from lib.params_camera import config
from lib.generate_pointcloud import generate_pointcloud

def make_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-rgb', '--rgbimage', default='demo/rgb.png')
	parser.add_argument(
		'-depth', '--depthimage', default='demo/depth.png')
	return parser

def plot_plane(a, b, c, d):
	xx, yy = np.mgrid[:5, :5]
	return xx, yy, (-d - a * xx - b * yy) / c

def rotate_view(vis):
	ctr = vis.get_view_control()
	ctr.rotate(10.0, 0.0)
	return False

if __name__ == '__main__':
        parser = make_parser()
        args = parser.parse_args()
        rgb = cv2.imread(args.rgbimage)
        depth = plt.imread(args.depthimage)
        #depth = csv2depth(args.depthimage)
        depth = depth / 255 * 1000
        depth[depth>3] = 0
        #depth = plt.imread(args.depthimage)
        #depth = pkl.load(open('depth.pkl','rb'))
        rgb = rgb[:depth.shape[0], :depth.shape[1]]
        rgb = np.array(rgb, dtype=np.float64)
        mask = np.ones(depth.shape)
        mask[depth==0] = 0
        pointcloud, dict_depth_point = rgbd2pointcloud(rgb, depth)
        pointcloud_ori = pointcloud.copy()
        pointcloud = random.sample(list(pointcloud), 500)
        pointcloud = np.array(pointcloud).reshape((-1,3))

        plane_detected, percentage_points_covered = ransac(pointcloud)
        for key in dict_depth_point.keys():
        	if np.dot(plane_detected, dict_depth_point[key]) < config.error_tolerated:
        		coordinates = eval(str(key))
        		mask[coordinates[0], coordinates[1]] = 0
        depth_of_plane = depth * mask
        depth_not_plane = depth * (1 - mask)
        rgb_of_plane = rgb.copy()
        for i in range(3):
            rgb_of_plane[:, :, i] *= mask
        rgb_of_plane = np.array(rgb_of_plane, dtype=np.uint8)
        plt.imsave(config.target_dir + 'rgb_of_plane.png', rgb_of_plane)
        plt.imsave(config.target_dir + 'depth_of_plane.png', depth_of_plane)
        plt.imsave(config.target_dir + 'depth_not_plane.png', depth_not_plane)
        plt.imsave(config.target_dir + 'mask_of_plane.png', mask)
        im = Image.open(config.target_dir+"rgb_of_plane.png").convert('RGB')
        im.save(config.target_dir+'rgb_of_plane.png')
        im_ = Image.open(config.target_dir+"depth_of_plane.png").convert('I')
        im_.save(config.target_dir+'depth_of_plane.png')
        generate_pointcloud(config.target_dir+'rgb_of_plane.png', config.target_dir+'depth_of_plane.png', 'output.ply')
