#!/usr/bin/env python

# Combines a folder of frames into a video using moviepy
#
# usage: $ python video.py 60  webcamImages {webcamTimelapse}
#                          fps directory    name
# If the name is omitted, the video will have the same name as the folder
# the images came from.

from moviepy.editor import *
import sys
import os

frames = int(sys.argv[1])
directory = sys.argv[2]

try:
    outputName = sys.argv[3] + '.mp4'
except Exception, e:
    outputName = directory + '.mp4'

# Pythonism ensues
names = [directory + '/' + name for name in os.listdir(directory) if name.endswith(".jpg")]
names.sort()

clip = ImageSequenceClip(names, fps = frames)
clip.write_videofile(outputName, fps = frames)
