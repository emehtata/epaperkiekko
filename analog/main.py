#!/usr/bin/env python3
"""Pysäköintikiekko e-paperilla"""

from datetime import datetime
import logging
import time
import math
import sys
from PIL import Image

# Importing custom modules
from my_epaper import epd2in7b
from my_clock import my_clock

# Setting up logging configuration
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s [%(filename)s:%(lineno)s - %(funcName)s()]',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

def analog_kiekko(h, m):
    """
    Generates and displays the analog clock image on the e-paper display.

    Parameters:
    h (int): Hour to display on the clock
    m (int): Minute to display on the clock
    """
    # Generate the clock image rotated and cropped based on the given time
    img = my_clock.rotate_and_crop_image(h, m)

    # Initialize the e-paper display
    epd = epd2in7b.EPD()
    epd.init()
    logging.info("Clear...")

    # Clear the display
    epd.Clear(0xFF)

    # Create new images for the display
    blackimage1 = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 264*176
    redimage1 = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 264*176

    # Paste the clock image onto the black image
    blackimage1.paste(img, (0, 0))

    # Display the images on the e-paper display
    epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))

if __name__ == "__main__":
    # Check for too many command-line arguments
    if len(sys.argv) > 2:
        print("Liikaa argumentteja. Käytä joko 'python script.py HH:MM' tai 'python script.py'.")
        sys.exit(1)

    # Check if a specific time is provided via command-line arguments
    if len(sys.argv) == 2:
        h, m = map(int, sys.argv[1].split(':'))
    else:
        # Default to the current system time
        current_time = datetime.now().time()
        h = current_time.hour
        m = current_time.minute

    force_update = True  # Flag to force an update on the first run
    last_update = datetime.now().time()  # Track the last update time

    while True:
        # Calculate the current time in half-hour increments
        current_time_half = math.ceil((h * 60 + m + 1) / 30)
        logging.info(current_time_half)

        # Check if an update is needed
        if force_update or (last_update != current_time_half):
            analog_kiekko(h, m)  # Update the display with the current time
            last_update = current_time_half  # Update the last update time

        # Sleep for 30 seconds before the next check
        time.sleep(30)

        # Update the current time
        current_time = datetime.now().time()
        h = current_time.hour
        m = current_time.minute
        force_update = False  # Reset the force update flag

