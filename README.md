# Plane_Detection_RGBD
Plane detection using single RGBD image

## Hardware
* realsense d415

## Dependencies
* Python 3
* numpy
* matplotlib
* pickle
* cv2
* ros
* pyrealsense

## Quick start
```
cd get_imgs_from_camera

# starting record videos
python3 record_camera.py

# extract images from recorded file
mkdir depth
mkdir rgb
python3 generate_rbgdepth_imgs.py

# segmenting the plane in the refered image
cd ..
python3 main.py

# segmented result will be saved in file "output.ply", which can be viewed by meshlab
```
