# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-FileCopyrightText: Adapted from Phil B.'s 16bit_hello Arduino Code
# SPDX-License-Identifier: MIT
# Updated 2026 at Iffy Books, wtfpl
# Updated 2026 by alinen: compute file list once; shorten display time

import gc
import time
import displayio
import picodvi
import board
import framebufferio

import busio
import sdcardio
import storage

# Or, use an SPI bus on specific pins:
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)

# For breakout boards, you can choose any GPIO pin that's convenient:
cs = board.GP5
# Boards with built in SPI SD card slots will generally have a
# pin called SD_CS:
#cs = board.SD_CS

sdcard = sdcardio.SDCard(spi, cs, False)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd") # NOTE: directory needs to already exist on the device

import os
imgs = [item for item in os.listdir("/sd/") if item[-4:].lower() == '.bmp']
print(imgs)

# pin defs for DVI Sock
displayio.release_displays()
fb = picodvi.Framebuffer(320, 240,
	clk_dp=board.GP14, clk_dn=board.GP15,
	red_dp=board.GP12, red_dn=board.GP13,
	green_dp=board.GP18, green_dn=board.GP19,
	blue_dp=board.GP16, blue_dn=board.GP17,
	color_depth=8)
display = framebufferio.FramebufferDisplay(fb)

bitmap = displayio.Bitmap(display.width, display.height, 3)

group = displayio.Group()

def clean_up(group_name):
    for _ in range(len(group_name)):
        group_name.pop()
    gc.collect()

def display_bitmap(path_name):
    gc.collect()
    blinka_bitmap = displayio.OnDiskBitmap(path_name)
    blinka_grid = displayio.TileGrid(blinka_bitmap, pixel_shader=blinka_bitmap.pixel_shader)
    gc.collect()
    group.append(blinka_grid)

    time.sleep(5)
    clean_up(group)

    del blinka_grid
    del blinka_bitmap
    gc.collect()

display.root_group = group
while True:
    for img_path in imgs:
        display_bitmap("/sd/"+img_path)
