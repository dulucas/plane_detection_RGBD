import os

os.system('rs-convert -i object_detection.bag -d -v depth/')
os.system('rs-convert -i object_detection.bag -c -p rgb/')
