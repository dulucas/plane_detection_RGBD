import numpy as np
import numpy as np
import cv2
import argparse
from lib.params_camera import config
import pickle as pkl
from lib.rgbd2pointcloud import rgbd2pointcloud
from lib.ransac import ransac
import matplotlib
import matplotlib.pyplot as plt
import random
import matplotlib.tri as mtri
import open3d as o3d
from lib.ransac import is_inlier
from lib.csv2depth import csv2depth
from sklearn.cluster import KMeans
plot_all = False

def make_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-rgb', '--rgbimage', default='rgb/_Color_300.png')
	parser.add_argument(
		'-depth', '--depthimage', default='depth/_Depth_300.csv')
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
        #depth = cv2.imread(args.depth, 0)
        #fig = plt.figure()
        #ax = mplot3d.Axes3D(fig)
        #depth = pkl.load(open(args.depthimage,'rb'))
        depth = csv2depth(args.depthimage)
        rgb = rgb[:depth.shape[0], :depth.shape[1]]
        #print(np.unique(depth))
        #rgb = np.zeros(depth.shape)
        pointcloud, dict_depth_point = rgbd2pointcloud(rgb, depth)
        pointcloud_ori = pointcloud
        pointcloud = random.sample(list(pointcloud), 500)
        pointcloud = np.array(pointcloud).reshape((-1,3))

        # Try to integrate RGB image
        '''
        volume = o3d.integration.ScalableTSDFVolume(voxel_length=4.0 / 512.0, sdf_trunc=0.04, color_type=o3d.integration.TSDFVolumeColorType.RGB8)
        color = o3d.io.read_image("imgs/NP2_132.jpg".format(0))
        depth = o3d.io.read_image("imgs/depth.png".format(0))
        rgbd = o3d.geometry.create_rgbd_image_from_color_and_depth(color, depth, depth_trunc=4.0, convert_rgb_to_intensity=False)
        volume.integrate(rgbd, o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault), config.extrinsic_parameters)
        mesh = volume.extract_triangle_mesh()
        mesh.compute_vertex_normals()
        o3d.visualization.draw_geometries([mesh])
        #pointcloud = random.sample(pointcloud, 500)
        #pointcloud = np.array(pointcloud).reshape((-1,3))
        # open3d example
        '''
        # Pass xyz to Open3D.o3d.geometry.PointCloud and visualize
        triang = mtri.Triangulation(pointcloud[:,0], pointcloud[:,1])
        z = (np.arange(pointcloud.shape[0]) + 1) / 100
        #rgb = np.random.random((500,500))
        #ax.scatter3D(pointcloud.T[0], pointcloud.T[1], pointcloud.T[2])
        #ax.plot_trisurf(triang, pointcloud[:,-1])
        #collec.set_array(colors)
        plane_detected, percentage_points_covered = ransac(pointcloud)
        a, b, c, d = plane_detected
        #xx, yy, zz = plot_plane(a, b, c, d)
        #ax.plot_surface(xx, yy, zz, color=(0, 1, 0, 0.5))
        #plt.show()
        #for key in dict_depth_point.keys():
        #	if np.dot(plane_detected, dict_depth_point[key]) < config.error_tolerated:
        #		coordinates = eval(str(key))
        #		mask[coordinates[0], coordinates[1]] = 255
        #depth_of_plane = depth * (mask > 1)
        #depth_not_plane = depth * (mask == 0)
        #rgb_of_plane = rgb * (mask > 2)
        #cv2.imwrite(config.target_dir + 'rgb_of_plane.png', rgb_of_plane)
        #cv2.imwrite(config.target_dir + 'depth_of_plane.png', depth_of_plane)
        #cv2.imwrite(config.target_dir + 'depth_not_plane.png', depth_not_plane)
        #cv2.imwrite(config.target_dir + 'mask_of_plane.png', mask)
        pointcloud_rest = []
        if plot_all:
            pointcloud_rest = pointcloud_ori
        else:
            for point in pointcloud_ori:
                if is_inlier(np.array(point), plane_detected, config.error_tolerated * 3):
                    continue
                pointcloud_rest.append(point)
        pointcloud_rest = np.array(pointcloud_rest).reshape((-1, 3))
        #print(pointcloud_rest.shape)
        print('Done!')
        classifier = KMeans(n_clusters=config.kmeans_clusters, random_state=0)
        classifier.fit(pointcloud_rest)
        labels = classifier.labels_
        indexs = np.ones(labels.shape)
        for label in range(config.kmeans_clusters):
            count_sum = np.sum(classifier.labels_==label)
            if count_sum < config.threhold_mesh:
                indexs[labels==label] = 0
        pointcloud_rest = pointcloud_rest[indexs>0]
        #from IPython import embed;embed()
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(pointcloud_rest)
        o3d.io.write_point_cloud("sync.ply", pcd)
        # Load saved point cloud and visualize it
        pcd_load = o3d.io.read_point_cloud("sync.ply")
        #o3d.visualization.draw_geometries([pcd_load])
        o3d.visualization.draw_geometries_with_animation_callback([pcd_load], rotate_view)
        #o3d.visualization.draw_geometries_with_editing([pcd_load])
        #camera_poses = read_trajectory("camera.log")
