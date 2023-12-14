#!/usr/bin/env python3
"""Pysäköintikiekko e-paperilla"""
import datetime
import logging
import os.path
import sys
import time

from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont

from my_epaper import epd2in7b
from my_settings import my_settings
from my_settings.my_status import MyStatus

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s [%(filename)s:%(lineno)s - %(funcName)s()]',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

status = MyStatus()

def handle_btn_press(btn):
    """Nappien käsittely"""
    pin_num = btn.pin.number
    saved_title = status.current_title
    status.current_title = my_settings.titles.get(pin_num, "Error")
    logging.info("Button pressed %d: %s", pin_num, status.current_title)
    if pin_num == 19:
        draw_kiekko(datetime.datetime.now().strftime("%H:%M"))
        time.sleep(60)
        status.current_title = saved_title
    status.force_update=True

def get_next_half_hour(my_status):
    """Hae seuraava tasapuolituntinen"""
    current_time = my_status.current_time
    if current_time:
        try:
            # Erottele syöte tunneiksi ja minuuteiksi.
            hours, minutes = map(int, current_time.split(':'))

            # Luo datetime-objekti annetusta ajasta.
            now = datetime.datetime.now().replace(
                hour=hours, minute=minutes, second=0, microsecond=0)
        except ValueError:
            print("Virheellinen aikaformaatti. Käytä HH:MM-muotoa.")
            sys.exit(1)
    else:
        now = datetime.datetime.now()

    # Tarkista, onko skripti käynnistetty ennen luomista.
    script_creation_time = datetime.datetime.fromtimestamp(os.path.getctime(__file__))
    while now < script_creation_time:
        logging.warning("Odota, kunnes laitteen kello on myöhempi kuin skriptin luomisaika...")
        logging.warning("%s < %s", now, script_creation_time)
        time.sleep(5)  # Odota 5 sekuntia ennen uutta tarkistusta
        now = datetime.datetime.now()


    # Laske aikaero seuraavaan puolen tuntiin.
    delta_minutes = 30 - (now.minute % 30)
    logging.debug("Laske aikaero seuraavaan puolen tuntiin: %d", delta_minutes)

    # Lisää aikaero nykyiseen aikaan.
    my_status.next_half_hour = now + datetime.timedelta(minutes=delta_minutes)

    # Nollaa sekunnit ja mikrosekunnit.
    my_status.next_half_hour = my_status.next_half_hour.replace(second=0, microsecond=0)

    logging.debug("Seuraava puolituntinen: %s", my_status.next_half_hour)
    return my_status

def draw_kiekko(timestring):
    """Piirrä pysäköintikiekko"""
    font_url = ImageFont.truetype(
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 12)

    font_title = ImageFont.truetype(
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)

    font_time = ImageFont.truetype(
        '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 108)

    epd = epd2in7b.EPD()
    epd.init()
    logging.info("Clear...")
    epd.Clear(0xFF)
    blackimage1 = Image.new(
        '1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 264*176
    redimage1 = Image.new(
        '1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)  # 264*176

    drawblack = ImageDraw.Draw(blackimage1)
    drawblack.text((50,1), f"{status.current_title}", font=font_title, fill=0)
    drawblack.text((1,30), f"{timestring}", font=font_time, fill=0)
    drawblack.text((1,148), f"epaperkiekko v{my_settings.version}", font=font_url, fill=0)
    drawblack.text((1,161), "https://github.com/emehtata/epaperkiekko", font=font_url, fill=0)

    epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))

def main_loop(my_status):
    """Pääohjelmasilmukka"""
    my_status.saved_half_hour = None
    while True:
        my_status = get_next_half_hour(my_status)
        my_status.current_time = None
        if(my_status.saved_half_hour != my_status.next_half_hour or my_status.force_update):
            formatted_time = my_status.next_half_hour.strftime("%H:%M")
            logging.info("Set time to: %s", formatted_time)
            draw_kiekko(formatted_time)
            my_status.force_update = False
        my_status.saved_half_hour = my_status.next_half_hour
        time.sleep(10)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Liikaa argumentteja. Käytä joko 'python script.py HH:MM' tai 'python script.py'.")
        sys.exit(1)

    if len(sys.argv) == 2:
        status.current_time = sys.argv[1]
    else:
        status.current_time = None

    buttons = [Button(5), Button(6), Button(13), Button(19)]
    for b in buttons:
        b.when_pressed = handle_btn_press

    # Silmukka, joka odottaa kellon päivittymistä.
    # Raspberry Pi on riippuvainen verkon ajasta, joten crontab ei ole luotettava.
    while True:
        main_loop(status)
