"""
stuur_robot.py: Bestuur de FLL-robot met je toetsenbord, via Bluetooth (BLE).

LET OP: dit programma draait op de COMPUTER (gewone Python), niet op de hub.
Het werkt samen met vrij_rijden.py, dat op de hub draait.
Uitleg voor beginners: zie README.md

Vereist:
    pip install bleak pynput

Werkwijze:
    1. Open Pybricks Code, verbind met de hub, laad vrij_rijden.py, maar
       druk NIET op 'run' -- druk gewoon op 'download' zodat het programma
       op de hub klaarstaat.
    2. Koppel Pybricks Code los van de hub (Bluetooth-icoontje).
    3. Start dit script: python stuur_robot.py
    4. Zodra hier "Verbonden!" verschijnt, druk je op de knop OP DE HUB
       zelf om vrij_rijden.py te starten.
    5. Bestuur de robot met ZQSD (AZERTY), zie de toetsen hieronder.

Na het tunen: zet main.py terug op de hub voor de wedstrijd!
"""

import asyncio
import datetime
from contextlib import suppress
from bleak import BleakScanner, BleakClient
from pynput import keyboard

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"

# Pas dit aan als je de hub in Pybricks Code een andere naam gaf
HUB_NAME = "githo botic"

LOGBESTAND = "rijlog.txt"

# --- TOETSEN ---
# Z / S       : vooruit / achteruit   (AZERTY-toetsenbord)
# Q / D       : draaien links / rechts
# I / K       : linker attachment vooruit / achteruit
# O / L       : rechter attachment vooruit / achteruit
# SHIFT       : ingedrukt houden voor een tragere, preciezere snelheid
# M           : stapmodus aan/uit (elke tik = 5 mm of 1 graad)
# R           : zet afstand/hoek/attachment-hoeken hier terug op 0
# SPATIE      : toon een kant-en-klare regel voor missies.py, en zet
#               daarna meteen het nulpunt (zoals R)
# ESC         : programma stoppen

# Welke toets op het toetsenbord welke actie doet. Wil je andere toetsen?
# Pas enkel de letters links aan.
TOETSEN = {
    "z": "vooruit",
    "q": "links",
    "s": "achteruit",
    "d": "rechts",
    "r": "nulpunt",
    "i": "links_att_plus",
    "k": "links_att_min",
    "o": "rechts_att_plus",
    "l": "rechts_att_min",
    "m": "stapmodus",
}

ingedrukte_toetsen = set()  # bevat de ACTIES (bv. "vooruit"), niet de letters
spatie_al_verwerkt = False
nulpunt_sturen = False      # True = stuur bij het volgende commando één keer "nulpunt"

laatste_waarden = {"afstand": 0, "hoek": 0, "links": 0, "rechts": 0}


def schrijf_log(tekst):
    """Schrijft één regel, met tijdstip, naar het logbestand op de computer."""
    tijd = datetime.datetime.now().strftime("%H:%M:%S")
    with open(LOGBESTAND, "a", encoding="utf-8") as bestand:
        bestand.write("[%s] %s\n" % (tijd, tekst))


def verwerk_hub_regel(tekst):
    """Leest een regel zoals 'afstand=245 hoek=12 links=0 rechts=-15' van de
    hub en onthoudt de laatste waarden, voor de spatiebalk-functie."""
    for deel in tekst.split():
        if "=" in deel:
            sleutel, _, waarde = deel.partition("=")
            if sleutel in laatste_waarden:
                try:
                    laatste_waarden[sleutel] = int(waarde)
                except ValueError:
                    pass


def toon_kopieerbare_stap():
    """Toont (en logt) kant-en-klare regels voor missies.py, op basis van de
    laatst ontvangen waarden van de hub.

    AANGEPAST: na het tonen zetten we meteen het nulpunt, net alsof je R
    indrukt. Vroeger telden de getallen op sinds de laatste keer dat je R
    drukte. Reed je rechtdoor en draaide je daarna, dan kreeg je bij de
    tweede SPATIE de TOTALE afstand, en niet de afstand van die ene stap.
    Nu is elke SPATIE precies één stap: rij, SPATIE, draai, SPATIE, ...
    Ook tonen we enkel nog de bewegingen die niet 0 zijn."""
    global nulpunt_sturen

    regels = []
    if laatste_waarden["afstand"] != 0:
        regels.append('("straight", %d),' % laatste_waarden["afstand"])
    if laatste_waarden["hoek"] != 0:
        regels.append('("turn", %d),' % laatste_waarden["hoek"])
    if abs(laatste_waarden["links"]) > 1:
        regels.append('("run_angle", LEFT_ATTACHMENT, 200, %d),' % laatste_waarden["links"])
    if abs(laatste_waarden["rechts"]) > 1:
        regels.append('("run_angle", RIGHT_ATTACHMENT, 200, %d),' % laatste_waarden["rechts"])

    print()
    if regels:
        print("Kopieerbaar voor missies.py:")
        for regel in regels:
            print("   ", regel)
        schrijf_log("STAP: " + " | ".join(regels))
    else:
        print("De robot is niet bewogen sinds het vorige nulpunt.")
    print()

    # Nulpunt zetten: de hub krijgt dit mee met het volgende commando
    # (zie maak_commando). Hier op de computer zetten we de onthouden
    # waarden ook al op 0, zodat een tweede SPATIE meteen klopt.
    nulpunt_sturen = True
    for sleutel in laatste_waarden:
        laatste_waarden[sleutel] = 0


def on_press(key):
    global spatie_al_verwerkt

    if key in (keyboard.Key.shift, keyboard.Key.shift_r):
        ingedrukte_toetsen.add("precisie")
        return

    if key == keyboard.Key.space:
        if not spatie_al_verwerkt:
            spatie_al_verwerkt = True
            toon_kopieerbare_stap()
        return

    try:
        letter = key.char.lower()
    except AttributeError:
        return
    if letter in TOETSEN:
        ingedrukte_toetsen.add(TOETSEN[letter])


def on_release(key):
    global spatie_al_verwerkt

    if key == keyboard.Key.esc:
        ingedrukte_toetsen.add("stoppen")
        return

    if key in (keyboard.Key.shift, keyboard.Key.shift_r):
        ingedrukte_toetsen.discard("precisie")
        return

    if key == keyboard.Key.space:
        spatie_al_verwerkt = False
        return

    try:
        letter = key.char.lower()
    except AttributeError:
        return
    if letter in TOETSEN:
        ingedrukte_toetsen.discard(TOETSEN[letter])


def maak_commando():
    """Bouwt het 12-tekens commando voor de hub, elk teken '1' of '0'.
    De volgorde moet exact overeenkomen met vrij_rijden.py op de hub."""
    global nulpunt_sturen

    # AANGEPAST: na SPATIE sturen we één keer "nulpunt" mee, net alsof R
    # kort ingedrukt werd. Daarna meteen weer uit, zodat de hub het ziet
    # als één tik. (Zo werkt het ook als je SPATIE heel kort aantikt.)
    toetsen = set(ingedrukte_toetsen)   # een kopie, het origineel blijft hetzelfde
    if nulpunt_sturen:
        toetsen.add("nulpunt")
        nulpunt_sturen = False

    volgorde = ("vooruit", "links", "achteruit", "rechts", "nulpunt", "stoppen",
                "links_att_plus", "links_att_min", "rechts_att_plus", "rechts_att_min",
                "precisie", "stapmodus")
    return "".join("1" if t in toetsen else "0" for t in volgorde).encode()


async def main():
    main_task = asyncio.current_task()

    def handle_disconnect(_):
        print("Verbinding met de hub verbroken.")
        schrijf_log("Verbinding verbroken.")
        if not main_task.done():
            main_task.cancel()

    ready_event = asyncio.Event()
    ontvangen = bytearray()  # buffer: Bluetooth knipt berichten in stukjes

    def handle_rx(_, data: bytearray):
        if data[0] != 0x01:  # enkel "write stdout"-events van de hub
            return
        ontvangen.extend(data[1:])

        # 1) Het "rdy"-signaal kan midden tussen andere tekst zitten, of over
        #    twee stukjes verdeeld zijn. Daarom zoeken we het in de buffer.
        while True:
            plaats = ontvangen.find(b"rdy")
            if plaats < 0:
                break
            del ontvangen[plaats:plaats + 3]
            ready_event.set()

        # 2) Enkel volledige regels (tot aan een Enter) tonen en verwerken
        while True:
            einde = ontvangen.find(b"\n")
            if einde < 0:
                break
            regel = bytes(ontvangen[:einde]).decode(errors="ignore").strip()
            del ontvangen[:einde + 1]
            if regel:
                print("Hub:", regel)
                verwerk_hub_regel(regel)
                schrijf_log("HUB: " + regel)

    schrijf_log("=== Nieuwe sessie gestart ===")
    print("Zoeken naar de hub (zorg dat Pybricks Code losgekoppeld is)...")
    device = await BleakScanner.find_device_by_name(HUB_NAME)
    if device is None:
        print("Kon de hub niet vinden.")
        print("- Staat Bluetooth aan op je computer?")
        print("- Is Pybricks Code losgekoppeld van de hub?")
        print("- Klopt HUB_NAME bovenaan dit bestand met de naam in Pybricks Code?")
        return

    async with BleakClient(device, handle_disconnect) as client:
        await client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, handle_rx)

        async def send(data):
            await ready_event.wait()
            ready_event.clear()
            await client.write_gatt_char(
                PYBRICKS_COMMAND_EVENT_CHAR_UUID,
                b"\x06" + data,  # "write stdin"-commando
                response=True,
            )

        luisteraar = keyboard.Listener(on_press=on_press, on_release=on_release)
        luisteraar.start()

        print("Verbonden! Druk nu op de knop OP DE HUB om vrij_rijden.py te starten.")
        print("Z/S=vooruit/achteruit  Q/D=draaien  I/K=linker attachment  O/L=rechter attachment")
        print("SHIFT=extra traag  M=stapmodus aan/uit  R=nulpunt hier  SPATIE=kopieerbare regel + nulpunt  ESC=stoppen")

        while "stoppen" not in ingedrukte_toetsen:
            await send(maak_commando())
            await asyncio.sleep(0.02)

        await send(maak_commando())  # laatste commando (met stoppen=1) sluit de hub-lus af
        luisteraar.stop()
        print("Gestopt.")
        schrijf_log("=== Sessie gestopt ===")


if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        asyncio.run(main())
