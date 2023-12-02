import datetime
import sys
import logging
logging.basicConfig(level=logging.INFO)

import epd2in7b
import my_version
from PIL import Image, ImageDraw, ImageFont

def get_next_half_hour(current_time=None):
    if current_time:
        try:
            # Erottele syöte tunneiksi ja minuuteiksi.
            hours, minutes = map(int, current_time.split(':'))

            # Luo datetime-objekti annetusta ajasta.
            now = datetime.datetime.now().replace(hour=hours, minute=minutes, second=0, microsecond=0)
        except ValueError:
            print("Virheellinen aikaformaatti. Käytä HH:MM-muotoa.")
            sys.exit(1)
    else:
        now = datetime.datetime.now()

    # Laske aikaero seuraavaan puolen tuntiin.
    delta_minutes = 30 - (now.minute % 30)

    # Lisää aikaero nykyiseen aikaan.
    next_half_hour = now + datetime.timedelta(minutes=delta_minutes)

    # Nollaa sekunnit ja mikrosekunnit.
    next_half_hour = next_half_hour.replace(second=0, microsecond=0)

    return next_half_hour

def draw_kiekko(timestring):
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
    drawblack.text((50,1), "Pysäköinti alkoi:", font=font_title, fill=0)
    drawblack.text((1,30), f"{timestring}", font=font_time, fill=0)
    drawblack.text((1,148), f"epaperkiekko v{my_version.version}", font=font_url, fill=0)
    drawblack.text((1,161), "https://github.com/emehtata/epaperkiekko", font=font_url, fill=0)

    epd.display(epd.getbuffer(blackimage1), epd.getbuffer(redimage1))

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Liikaa argumentteja. Käytä joko 'python script.py HH:MM' tai 'python script.py'.")
        sys.exit(1)

    if len(sys.argv) == 2:
        current_time = sys.argv[1]
    else:
        current_time = None

    next_half_hour = get_next_half_hour(current_time)

    formatted_time = next_half_hour.strftime("%H:%M")
    logging.info(f"Set time to: {formatted_time}")

    draw_kiekko(formatted_time)
