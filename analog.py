#!/usr/bin/env python3
"""Pysäköintikiekko e-paperilla"""
from datetime import datetime
import logging
import time
import math

from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont

from my_epaper import epd2in7b
from my_clock import my_clock

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s [%(filename)s:%(lineno)s - %(funcName)s()]',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def analog_kiekko(current_time):
    img = my_clock.rotate_and_crop_image(current_time)
    epd = epd2in7b.EPD()
    epd.init()
    logging.info("Clear...")
    epd.Clear(0xFF)
    blackimage1 = Image.new(
        '1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 264*176
    redimage1 = Image.new(
        '1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 264*176

    blackimage1.paste(img, (0,0))

    # drawblack = ImageDraw.Draw(blackimage1)

    epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))

if __name__ == "__main__":
    force_update =True
    last_update = datetime.now().time()

    while True:
        # Hae nykyinen aika
        current_time = datetime.now().time()
        current_time_half = math.ceil( ( current_time.hour * 60 + current_time.minute ) / 30)
        logging.info(current_time_half)
        if force_update or ( last_update != current_time_half ):
            analog_kiekko(current_time)
            last_update = current_time_half
        time.sleep(30)
        force_update = False
