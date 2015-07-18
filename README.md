# Webcam Timelapse

This python script (webcam.py) creates timelapse videos using webcam images. Usage is as follows:

    $ python webcam.py 10 4h webcamImages http://example.com/webcam.jpg

where:

- 10 is the interval between images in seconds.

- 4h is the time to keep recording. You can use d, h, or m for days, hours and minutes respectively.

- webcamImages is the name of the folder the images will be saved in. It will be created in the current working directory (os.getcwd()), i.e. the directory that the script is located in.

- http://webcam.com/current.jpg is the URL of the webcam images. A good way to find webcams that refresh constantly is to search google for "inurl:/axis-cgi/jpg/image.cgi". This particular type of webcams refreshes constantly, so you can take multiple images a second (given your bandwith is enough). Other webcams can be found on webcams.travel, but many of them only update every 15 min or less.

After the specified time is over, the script will use moviepy to create a 60fps video out of the images. If you want another framerate, use video.py (or moviepy directly from the console, or ffmpeg, or your favourite video editing software).