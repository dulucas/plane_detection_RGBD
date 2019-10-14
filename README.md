# Plane_Detection_RGBD
Plane detection using single RGBD image

## Hardware
* realsense d415

## Dependencies
* Python 3
* numpy
* matplotlib
* open3d
* pickle
* cv2
* sklearn
* ros
* pyrealsense

## Quick start
```
cd get_imgs_from_camera
python3 record_camera.py
mkdir depth
mkdir rgb
python3 generate_rbgdepth_imgs.py
cd ..
python3 main.py
```
