# epaperkiekko - pysäköintikiekko

Tämä python-skripti ohjelmoi Waveshare 2,7-tuuman epaper-näytön näyttämään kellonajan seuraavaan tasa- tai puoleen tuntiin, eli sitä voi käyttää automaattisena pysäköintikiekkona.

![alt text](doc/epaperkiekko.jpg)

## Tarvikkeet

* Raspberry Pi (3/4/5)
* epaper-näyttö ( tuettu Waveshare 2,7" b-version, https://www.waveshare.com/2.7inch-e-Paper-HAT-B.htm )
* Nettiyhteys konfiguroituna (kellon synkronointia varten), esim. jakamalla puhelimen hotspotilla

## Käyttö

Käännä image:

    make build

Käynnistä kontti:

    make run

Lisää tietoja `Makefile`-tiedostossa.

Autossa:

1. Varmista, että sinulla on toimiva nettiyhteys jaettuna Raspberry Pille
1. Kytke usb-johto syöttämään virta Raspberry Pille
1. Lähde ajamaan
1. Näyttö päivittyy laitteen käynnistyttyä sekä tasa- ja puolitunnein
1. Pysäköi auto
1. Irrota Raspberry Pi virransyötöstä (useimmiten auton sammuttaminen riittää) ja aseta se kojelaudalle. Se näyttää nyt automaattisesti seuraavaa tasa- tai puolta tuntia, kuten pysäköintikiekon kuuluukin \o/
1. Kun olet hoitanut asiasi, palaa kohtaan 1.

Nappien toiminnot vasemmalta ylhäältä alas:
* Aseta teksti "Saapumisaika" (Oletus)
* Aseta teksti "Ankomstid"
* Aseta teksti "Pysäköinti alkoi"
* Näytä kellonaika

## Testaus

    python3 main.py (Aika järjestelmän kellosta)

    python3 main.py HH:MM (Aika komentoriviparametrina)

## "Analoginen" versio (Työn alla)

    python3 analog.py (Näyttää oikean parkkikiekon kuvan)

## TODO

* Tallenna asetukset ja lue ne käynnistyksessä
