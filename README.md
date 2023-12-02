# epaperkiekko - pysäköintikiekko

## Tarvikkeet

* Raspberry Pi (3/4/5)
* epaper-näyttö (Waveshare 2,7", https://www.waveshare.com/2.7inch-e-paper-hat.htm)
* OS, jossa valmiiksi konfattu python3 epaperpi-kirjastoineen (tämän dokumentin ulkopuolella)

## Käyttö

crontab (muuta polku):

    @reboot sleep 10 && cd /home/pi/work/epaperkiekko && python3 main.py
    */30 * * * * cd /home/pi/work/epaperkiekko && python3 main.py

Testaus:

    python3 main.py (Aika järjestelmän kellosta)

    python3 main.py HH:MM (Aika komentoriviparametrina)
