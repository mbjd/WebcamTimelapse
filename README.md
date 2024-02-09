# Webcam Timelapse

This python script (webcam.py) creates timelapse videos using webcam images. Usage is as follows:

    $ ./webcam.py 10 4h webcamImages http://example.com/webcam.jpg

where:

- 10 is the interval between images in seconds.

- 4h is the time to keep recording. You can use d, h, m, or s for days, hours, minutes and seconds respectively.

- webcamImages is the name of the folder the images will be saved in. It will be created in the current working directory, determined by `os.getcwd()`

- http://example.com/webcam.jpg is the URL of the webcam image. A good way to find webcams is to search google for `inurl:"/axis-cgi/jpg/image.cgi"`. This particular type of webcam refreshes constantly, so you can take multiple images a second (given your bandwith is enough). Other webcams can be found on webcams.travel, but many of them only update every 15 min or less.

After the specified time is over, the script will use moviepy to create a 60fps video out of the images. If you want another framerate, use video.py (or moviepy directly from the console, or ffmpeg, or your favourite video editing software).


# update

This is a very old project and I've learned to be more pragmatic since. The whole thing can be done with two bash one-liners. The first one here to download images: 

    $ while true; do echo $URL; sleep 1; done | xargs -P8 -I{} sh -c 'wget -O ./webcam_images/$(date +%s.%N.jpg) {}'

this uses 8 parallel threads to start downloading the next image even if previous ones are still downloading (obviously still limited by bandwidth and possibly the server which might refuse responding to many requests quickly). Stop it with `^C` whenever you like, or modify the loop in the beginning. After that, use [ffmpeg to combine them](https://stackoverflow.com/questions/24961127/how-to-create-a-video-from-images-with-ffmpeg).

# update 2

If an `mjpg` stream is available (if the URL is `..../axis-cgi/jpg/image.cgi` there is usually a stream at `.../axis-cgi/mjpg/video.cgi`), it can also be recorded directly with `ffmpeg`! 

    ffmpeg -f mjpeg -framerate 30 -i 'https://83.77.144.55/axis-cgi/mjpg/video.cgi?fps=4' -c:v copy out.mp4

The `fps` in the url modifies the udpate rate of the stream, and the one given to `ffmpeg` determines the one in the final video file, so by playing with them you can modify the speedup ratio. Stop this whenever you are satisfied by pressing `q`. Somehow it only works if the IP is used in the URL, so if you have a domain name find the IP `dig`, `ping` or similar. Also sometimes it randomly stops, so the method above may be more reliable.

