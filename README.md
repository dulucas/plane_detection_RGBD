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
* PIL
* ros
* pyrealsense

## Quick start
```
# starting record videos
cd get_imgs_from_camera
python3 record_camera.py

# extract images from recorded file
mkdir depth
mkdir rgb
python3 generate_rbgdepth_imgs.py

# segmenting the plane in the refered image
cd ..
python3 main.py -rgb /DIR/TO/RBG/IMAGE -depth /DIR/TO/DEPTH/IMAGE

# segmented result will be saved in file "output.ply", which can be viewed by meshlab
```
## Demo
```
python3 main.py -rgb demo/rgb.png -depth demo/depth.png
```
PS : The rgb image and the depth image in the demo file do not match strictly...
