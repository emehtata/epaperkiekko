#!/usr/bin/env python3
"""Pysäköintikiekko e-paperilla"""
from datetime import datetime
import logging
import time
import math
import sys

from PIL import Image

from my_epaper import epd2in7b
from my_clock import my_clock

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s [%(filename)s:%(lineno)s - %(funcName)s()]',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def analog_kiekko(h, m):
    img = my_clock.rotate_and_crop_image(h, m)
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
    if len(sys.argv) > 2:
        print("Liikaa argumentteja. Käytä joko 'python script.py HH:MM' tai 'python script.py'.")
        sys.exit(1)

    if len(sys.argv) == 2:
        h,m = map(int, sys.argv[1].split(':'))
    else:
        current_time = datetime.now().time()
        h = current_time.hour
        m = current_time.minute

    force_update =True
    last_update = datetime.now().time()

    while True:
        # Hae nykyinen aika
        current_time_half = math.ceil( ( h * 60 + m+1 ) / 30)
        logging.info(current_time_half)
        if force_update or ( last_update != current_time_half ):
            analog_kiekko(h, m)
            last_update = current_time_half
        time.sleep(30)
        current_time = datetime.now().time()
        h = current_time.hour
        m = current_time.minute
        force_update = False
