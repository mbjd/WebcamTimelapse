#!/usr/bin/env python

# Combines a folder of frames into a video using moviepy
#
# usage: $ python video.py 60  webcamImages {webcamTimelapse}
#                          fps directory    name
# If the name is omitted, the video will have the same name as the folder
# the images came from.

from __future__ import print_function

from moviepy.editor import *
import sys
import os

frames = int(sys.argv[1])
directory = sys.argv[2]

try:
    # Append '.mp4' to the filename if it doesn't already end like that
    if sys.argv[3].endswith('.mp4'):
        outputName = sys.argv[3]
    else:
        outputName = sys.argv[3] + '.mp4'
except IndexError:
    outputName = directory.strip('/') + '.mp4'

# Pythonism ensues
names = [directory + '/' + name for name in os.listdir(directory) if name.endswith(".jpg") or name.endswith(".jpeg")]

if len(names) == 0:
    print('No files found', file=sys.stderr)
    sys.exit(1)
names.sort()

clip = ImageSequenceClip(names, fps=frames)
clip.write_videofile(outputName, fps=frames, codec='libx264')
