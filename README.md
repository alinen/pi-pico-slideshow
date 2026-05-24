# pi-pico-slideshow
Simple slideshow application for the Pi Pico based on CircuitPython

## How to build and run

This project is based on the [Iffy Books Pixel Buddy Video Player](https://iffybooks.net/pixel-buddy/).

This demo was tested using [Thony](https://thonny.org/). Setup summary:

* Install `adafruit-circuitpython-raspberry_pi_pico-en_US-10.2.1.uf2`
* Upload the contents of slideshow-src to the device
* Copy the files your want to show to your micro-SD

## Processing images

The images need to be at most 320x240 and have up to 16 bit color in bitmap format. 
for example, to convert all PNG images stored in the directory SRC we can do the 
following, using `convert` from imagemagick.

```
find SRC -name "*.png" -exec convert {} -resize 320x240 -depth 8 {}.bmp \;
``` 


