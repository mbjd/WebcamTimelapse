#
#  ### Program for making timelapse out of webcam images ###
#  
#  usage: $ python webcam.py 3 2d webcamImages http://webcam.com/current.jpg
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
#

from moviepy.editor import *
import threading
import urllib
import time
import sys
import os

# Process arguments
period = float(sys.argv[1])
folder = str(sys.argv[3])
url    = str(sys.argv[4])

duration = int(sys.argv[2][:-1])

if sys.argv[2].endswith("d"):
    endTime = time.time() + 24 * 60 * 60 * duration
elif sys.argv[2].endswith("h"):
    endTime = time.time() + 60 * 60 * duration
elif sys.argv[2].endswith("m"):
    endTime = time.time() + 60 * duration

# Directory stuff
homeDirectory = os.getcwd()
absPath = homeDirectory + '/' + folder

if not os.path.exists(folder):
    os.makedirs(folder)

def downloadImage(url, dir, name):
    image = urllib.URLopener()
    os.chdir(dir)
    image.retrieve(url, name)
    print('Saved image: ' + folder + '/' + name)
    os.chdir(homeDirectory)

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

    time.sleep(0.1)

# Make the video - 60fps default
outputName = folder + '.mp4'
names = [folder + '/' + name for name in os.listdir(folder) if name.endswith(".jpg")]

clip = ImageSequenceClip(names, fps = 60)
clip.write_videofile(outputName, fps = 60)