#!/usr/bin/env python

#
#  ### Program for making timelapse out of webcam images ###
#  
#  usage: $ ./webcam.py 3 2d webcamImages http://webcam.com/current.jpg
#  
#  3: interval between images in seconds
#  2d: How long to keep recording (X d/h/m)
#  webcamImages: Name of the folder to save images. Will be created in getcwd()
#  http://webcam.com/current.jpg: URL of the current image
#  
#  After the specified time has elapsed, a video will be created at 60 fps.
#  If you want to make another video at another framerate, use video.py.
#
#  Some webcam urls to try:
# 
#  http://hgwwebcam.dyndns.org:5000/axis-cgi/jpg/image.cgi   Sailboats, ZH, CH
#  http://80.75.114.18/axis-cgi/jpg/image.cgi?clock=1&text=0 KVA Horgen -> ZH
#  http://80.75.114.19/axis-cgi/jpg/image.cgi?clock=1&text=0 KVA Horgen -> Rappi
#  http://webcam.bodmer-chur.ch:8080/axis-cgi/jpg/image.cgi  Chur, CH
#  http://bautzen.redirectme.net/axis-cgi/jpg/image.cgi      German Airport
#  http://194.218.96.90/axis-cgi/jpg/image.cgi               Swedish Village
#  http://axis-lyss.axiscam.net:8080/axis-cgi/jpg/image.cgi  Geneva Roundabout
#  http://80.254.173.253:8080/axis-cgi/jpg/image.cgi         Interlaken, CH
#  http://146.186.123.229/axis-cgi/jpg/image.cgi             Penn State
#  http://77.106.162.110:8081/axis-cgi/jpg/image.cgi         Ski resort
#  http://webcam01.bigskyresort.com/axis-cgi/jpg/image.cgi   Ski resort
#  http://wc1.bluffton.edu/axis-cgi/jpg/image.cgi?resolution=2048x1536
#  http://62.202.23.123/record/current.jpg                   Lake Zurich
#  http://62.202.21.101/record/current.jpg                   Hotel somewhere
#  http://www.hoteltell.ch/Webcam/current.jpg                Schwyz, CH (only every min)
#  http://www.altenburg.eu/WebCam1/axis-cgi/jpg/image.cgi    Altenburg, CH
#  http://212.254.182.126/axis-cgi/jpg/image.cgi             Niesen, CH
#  http://213.213.183.83/SnapshotJPEG?Resolution=640x480     Bern, CH
#  http://213.221.150.136/axis-cgi/jpg/image.cgi             Monthey, CH
#  http://hogakusten.mine.nu/axis-cgi/jpg/image.cgi          Bridge in Sweden
#  https://s3-eu-west-1.amazonaws.com/felsenegg-cam/cam0.jpg Restaurant Felsenegg
#  http://46.140.114.222:8080/axis-cgi/jpg/image.cgi         Balkon
#  http://178.198.19.229/axis-cgi/jpg/image.cgi              UAV Lab
#  http://178.198.70.22/axis-cgi/jpg/image.cgi               Camping
#  http://212.243.94.2/axis-cgi/jpg/image.cgi                Honegg bei Buochs
#  http://178.199.206.91/axis-cgi/jpg/image.cgi              Amateur radio shop
#  http://46.150.196.132/cgi-bin/jpg/image.cgi               Roundabout
#  http://axis.meisal.com/axis-cgi/jpg/image.cgi             Fjellgrend, Norway
#  http://posta.mukolin.cz/axis-cgi/jpg/image.cgi            Czech (?) town square
#
#  ... http://members.upc.nl/a.horlings/doc-google.html
#

from moviepy.editor import *
import threading
import requests
import time
import sys
import os

# Process arguments
period = float(sys.argv[1])
folder = str(sys.argv[3])
url    = str(sys.argv[4])

duration = int(sys.argv[2][:-1])

# Convert duration of recording to seconds
if sys.argv[2].endswith("d"):
    endTime = time.time() + 24 * 60 * 60 * duration
elif sys.argv[2].endswith("h"):
    endTime = time.time() + 60 * 60 * duration
elif sys.argv[2].endswith("m"):
    endTime = time.time() + 60 * duration
elif sys.argv[2].endswith("s"):
    endTime = time.time() + duration
else:
    print("Invalid argument: sys.argv[2] must be an integer + 'd', 'h', 'm' or 's'")


# Directory stuff
homeDirectory = os.getcwd()
absPath = homeDirectory + '/' + folder

if not os.path.exists(folder):
    os.makedirs(folder)

# Downloader function
def downloadImage(url, dir, name):
    f = open(os.path.join(dir, name), 'wb')
    f.write(requests.get(url).content)
    f.close()

    print('Saved image: ' + folder + '/' + name)

# Timing
nextTime = time.time()
currentTime = time.time()

# Get the images for as long as specified
while currentTime < endTime:
    currentTime = time.time()

    if currentTime >= nextTime:
        nextTime += period

        timeStr = '{0}.jpg'.format(int(currentTime))
        downloadImage(url, folder, timeStr)

    # Sleep 0.1 seconds to make sure nothing is missed
    # Also you can set the interval to something like 0.3 secs
    time.sleep(0.1)

# Make the video - 60fps default
outputName = folder + '.mp4'
names = [folder + '/' + name for name in os.listdir(folder) if name.endswith(".jpg")]
names.sort()

clip = ImageSequenceClip(names, fps = 60)
clip.write_videofile(outputName, fps = 60)
