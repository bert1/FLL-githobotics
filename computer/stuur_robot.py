"""
stuur_robot.py: Bestuur de FLL-robot met je toetsenbord, via Bluetooth (BLE).

LET OP: dit programma draait op de COMPUTER (gewone Python), niet op de hub.
Het werkt samen met vrij_rijden.py, dat op de hub draait.
Uitleg voor beginners: zie docs/4-uitleg-code.md op GitHub

Vereist:
    pip install bleak pynput

Werkwijze:
    1. Zet de code op de hub met Pybricks Code zoals altijd (main.py).
       Druk niet op 'run', laat het programma gewoon op de hub staan.
    2. Koppel Pybricks Code los van de hub (Bluetooth-icoontje).
    3. Start dit script: python stuur_robot.py
    4. Zodra hier "Verbonden!" verschijnt, druk je op de knop OP DE HUB
       zelf om main.py te starten. Kies in het menu de letter V en druk
       op de middelste knop.
    5. Bestuur de robot met ZQSD (AZERTY), zie de toetsen hieronder.
       Alles wat je rijdt, wordt opgenomen in opname.txt.

AANGEPAST: vroeger moest je vrij_rijden.py op de hub zetten en daarna
main.py terugzetten voor de wedstrijd. Dat hoeft niet meer: vrij rijden
zit in het menu van main.py (letter V). vrij_rijden.py zelf starten kan
ook nog altijd.
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
# AANGEPAST (nieuw): hier komen de opgenomen stappen, klaar om te plakken
OPNAMEBESTAND = "opname.txt"

# AANGEPAST (nieuw): moet hetzelfde getal zijn als PROTOCOL in vrij_rijden.py
PROTOCOL = 2

# --- TOETSEN ---
# Z / S       : vooruit / achteruit   (AZERTY-toetsenbord)
# Q / D       : draaien links / rechts
# Z + Q of D  : een bocht rijden
# I / K       : linker attachment vooruit / achteruit
# O / L       : rechter attachment vooruit / achteruit
# SHIFT       : ingedrukt houden voor een tragere, preciezere snelheid
# M           : stapmodus aan/uit (elke tik = één kleine, exacte stap)
# 1 / 2 / 3   : stapgrootte in stapmodus: fijn / normaal / grof
# SPATIE      : de huidige stap nu afsluiten
# ENTER       : de huidige stap afsluiten en de hele opname tonen
# BACKSPACE   : laatste stap wissen, de robot rijdt terug
# R           : opname wissen en opnieuw beginnen (nulpunt hier)
# ESC         : programma stoppen

# Welke toets op het toetsenbord welke actie doet, zolang je ze INGEDRUKT
# HOUDT. Wil je andere toetsen? Pas enkel de letters links aan.
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

# AANGEPAST (nieuw): de cijfertoetsen voor de stapgrootte. Op een AZERTY-
# toetsenbord geven de cijfers bovenaan zonder SHIFT de tekens & é " ,
# daarom staan die er ook bij.
STAPGROOTTE_TOETSEN = {
    "1": "1", "&": "1",
    "2": "2", "é": "2",
    "3": "3", '"': "3",
}

ingedrukte_toetsen = set()  # bevat de ACTIES (bv. "vooruit"), niet de letters
# AANGEPAST (nieuw): acties die maar ÉÉN keer verstuurd worden (bv. SPATIE),
# ook als je de toets heel kort aantikt of lang vasthoudt
eenmalige_acties = set()
# Toetsen die nu fysiek ingedrukt zijn. Houd je een toets lang vast, dan
# stuurt de computer die toets steeds opnieuw ("autorepeat"). Zo herkennen
# we dat en tellen we het maar één keer.
al_ingedrukt = set()
stapgrootte = "2"
toon_alles_na_klaar = False     # True = na de volgende KLAAR de hele opname tonen

# AANGEPAST (nieuw): een kopie van de opname op de hub
opname = []                     # de stappen als tekst, bv. '("straight", 412),'
eerste_nummer = 0               # het stapnummer van de eerste stap
live_regel_getoond = False      # staat er nu een "nu: ..."-regel op het scherm?


def schrijf_log(tekst):
    """Schrijft één regel, met tijdstip, naar het logbestand op de computer."""
    tijd = datetime.datetime.now().strftime("%H:%M:%S")
    with open(LOGBESTAND, "a", encoding="utf-8") as bestand:
        bestand.write("[%s] %s\n" % (tijd, tekst))


def toon(tekst=""):
    """AANGEPAST (nieuw): print een gewone regel. Staat er een "nu: ..."-
    regel, dan wissen we die eerst, zodat de tekst niet door elkaar loopt."""
    global live_regel_getoond
    if live_regel_getoond:
        print("\r" + " " * 70 + "\r", end="")
        live_regel_getoond = False
    print(tekst)


def toon_live(tekst):
    """AANGEPAST (nieuw): de metingen van de huidige stap komen 10 keer per
    seconde binnen. In plaats van 10 nieuwe regels per seconde, schrijven
    we telkens over dezelfde regel. "\\r" springt terug naar het begin van
    de regel."""
    global live_regel_getoond
    print("\r" + tekst.ljust(70), end="", flush=True)
    live_regel_getoond = True


def opname_als_tekst():
    """Maakt de tekst voor opname.txt: de stappen met hun nummer."""
    tijd = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    regels = [
        "# Opname van stuur_robot.py (" + tijd + ")",
        "# Kopieer de stappen naar je missie in missies.py, boven de regel",
        '# ("call", stop_attachments). Het nummer achter # is het stapnummer.',
    ]
    for i, stap in enumerate(opname):
        regels.append("    " + stap.ljust(48) + "# stap " + str(eerste_nummer + i))
    if not opname:
        regels.append("# (nog geen stappen)")
    return "\n".join(regels) + "\n"


def schrijf_opname():
    """Zet de opname in opname.txt. Dit gebeurt na ELKE wijziging, zodat
    het bestand altijd klopt, ook als het programma plots stopt."""
    with open(OPNAMEBESTAND, "w", encoding="utf-8") as bestand:
        bestand.write(opname_als_tekst())


def verwerk_hub_regel(tekst):
    """AANGEPAST: leest een regel van de hub. Regels die beginnen met
    NIEUW, STAP of WEG houden de opname bij, "nu ..." toont de metingen.
    Geeft True terug als de regel verwerkt is, anders False."""
    global eerste_nummer, toon_alles_na_klaar
    delen = tekst.split(" ", 2)    # hoogstens in 3 stukken knippen

    if delen[0] == "nu":
        toon_live("Deze stap: " + tekst[3:])
        return True

    if delen[0] == "NIEUW" and len(delen) >= 2:
        eerste_nummer = int(delen[1])
        opname.clear()
        schrijf_opname()
        toon("Nieuwe opname. De eerste stap krijgt nummer " + str(eerste_nummer) + ".")
        return True

    if delen[0] == "STAP" and len(delen) == 3:
        plaats = int(delen[1]) - eerste_nummer
        del opname[plaats:]      # alles vanaf deze plaats weg (meestal niets)
        opname.append(delen[2])
        schrijf_opname()
        toon("Stap " + delen[1] + ":  " + delen[2])
        schrijf_log("STAP " + delen[1] + ": " + delen[2])
        return True

    if delen[0] == "WEG" and len(delen) >= 2:
        plaats = int(delen[1]) - eerste_nummer
        del opname[plaats:]
        schrijf_opname()
        toon("Stap " + delen[1] + " gewist, de robot reed terug.")
        schrijf_log("WEG stap " + delen[1])
        return True

    if delen[0] == "KLAAR":
        if toon_alles_na_klaar:
            toon_alles_na_klaar = False
            toon()
            toon(opname_als_tekst())
        return True

    return False


def on_press(key):
    global stapgrootte, toon_alles_na_klaar

    # AANGEPAST: een toets die al ingedrukt was (autorepeat) negeren
    try:
        naam = key.char.lower()
    except AttributeError:
        naam = key           # een speciale toets zoals SPATIE of ENTER
    if naam in al_ingedrukt:
        return
    al_ingedrukt.add(naam)

    if key in (keyboard.Key.shift, keyboard.Key.shift_r):
        ingedrukte_toetsen.add("precisie")
        return

    # AANGEPAST (nieuw): de toetsen die één keer iets doen
    if key == keyboard.Key.space:
        eenmalige_acties.add("stap_klaar")
        return
    if key == keyboard.Key.enter:
        eenmalige_acties.add("stap_klaar")
        toon_alles_na_klaar = True
        return
    if key == keyboard.Key.backspace:
        eenmalige_acties.add("ongedaan")
        return

    # Cijfertoetsen op het numeriek klavier hebben soms geen teken, enkel
    # een codenummer (vk). 97, 98, 99 zijn de toetsen 1, 2, 3 (Windows).
    vk = getattr(key, "vk", None)
    if vk in (97, 98, 99):
        stapgrootte = str(vk - 96)
        return

    if not isinstance(naam, str):
        return
    if naam in STAPGROOTTE_TOETSEN:
        stapgrootte = STAPGROOTTE_TOETSEN[naam]
        return
    if naam in TOETSEN:
        ingedrukte_toetsen.add(TOETSEN[naam])


def on_release(key):
    try:
        naam = key.char.lower()
    except AttributeError:
        naam = key
    al_ingedrukt.discard(naam)

    if key == keyboard.Key.esc:
        ingedrukte_toetsen.add("stoppen")
        return

    if key in (keyboard.Key.shift, keyboard.Key.shift_r):
        ingedrukte_toetsen.discard("precisie")
        # AANGEPAST: met SHIFT ingedrukt kan een letter als hoofdletter
        # "losgelaten" worden. Voor de zekerheid alles loslaten.
        al_ingedrukt.clear()
        return

    if isinstance(naam, str) and naam in TOETSEN:
        ingedrukte_toetsen.discard(TOETSEN[naam])


def maak_commando():
    """Bouwt het commando voor de hub: 14 tekens '1' of '0', dan de
    stapgrootte ("1", "2" of "3") en een Enter-teken (\\n) op het einde.
    De volgorde moet exact overeenkomen met vrij_rijden.py op de hub."""
    # AANGEPAST: de eenmalige acties worden één keer meegestuurd en daarna
    # meteen gewist. De hub ziet ze zo als één tik.
    toetsen = set(ingedrukte_toetsen)   # een kopie, het origineel blijft hetzelfde
    toetsen.update(eenmalige_acties)    # update() voegt een hele verzameling toe
    eenmalige_acties.clear()

    volgorde = ("vooruit", "links", "achteruit", "rechts", "nulpunt", "stoppen",
                "links_att_plus", "links_att_min", "rechts_att_plus", "rechts_att_min",
                "precisie", "stapmodus", "stap_klaar", "ongedaan")
    bits = "".join("1" if t in toetsen else "0" for t in volgorde)
    return (bits + stapgrootte + "\n").encode()


async def main():
    main_task = asyncio.current_task()

    def handle_disconnect(_):
        toon("Verbinding met de hub verbroken.")
        schrijf_log("Verbinding verbroken.")
        if not main_task.done():
            main_task.cancel()

    ready_event = asyncio.Event()
    protocol_ok = asyncio.Event()   # AANGEPAST: de hub heeft de juiste versie
    einde_event = asyncio.Event()   # AANGEPAST: de hub is klaar met afsluiten
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
            if not regel:
                continue

            # AANGEPAST (nieuw): klopt de versie van de hub?
            if regel.startswith("PROTOCOL"):
                if regel == "PROTOCOL %d" % PROTOCOL:
                    protocol_ok.set()
                else:
                    toon("Hub: " + regel)
                    toon("Deze stuur_robot.py past niet bij de code op de hub.")
                    toon("Download de nieuwste versie van allebei.")
                continue
            if regel.startswith("Klaar om te rijden"):
                # zo begon de OUDE vrij_rijden.py
                toon("De hub heeft een oude vrij_rijden.py. Zet de nieuwste code op de hub.")
                continue
            if regel == "EINDE":
                einde_event.set()
                continue

            if not verwerk_hub_regel(regel):
                toon("Hub: " + regel)
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
            await protocol_ok.wait()
            await ready_event.wait()
            ready_event.clear()
            await client.write_gatt_char(
                PYBRICKS_COMMAND_EVENT_CHAR_UUID,
                b"\x06" + data,  # "write stdin"-commando
                response=True,
            )

        luisteraar = keyboard.Listener(on_press=on_press, on_release=on_release)
        luisteraar.start()

        print("Verbonden! Druk nu op de knop OP DE HUB om main.py te starten,")
        print("kies de letter V en druk op de middelste knop.")
        print("Z/S=vooruit/achteruit  Q/D=draaien  I/K=linker attachment  O/L=rechter attachment")
        print("SHIFT=extra traag  M=stapmodus  1/2/3=stapgrootte  R=nieuwe opname  ESC=stoppen")
        print("SPATIE=stap afsluiten  ENTER=hele opname tonen  BACKSPACE=laatste stap terug")
        print("De opname staat altijd in", OPNAMEBESTAND)

        while "stoppen" not in ingedrukte_toetsen:
            await send(maak_commando())
            await asyncio.sleep(0.02)

        await send(maak_commando())  # laatste commando (met stoppen=1) sluit de hub-lus af
        luisteraar.stop()
        # AANGEPAST: even wachten tot de hub de laatste stap doorstuurde
        with suppress(asyncio.TimeoutError):
            await asyncio.wait_for(einde_event.wait(), 3)
        toon()
        toon(opname_als_tekst())
        toon("Gestopt. De opname staat in " + OPNAMEBESTAND)
        schrijf_log("=== Sessie gestopt ===")


if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        asyncio.run(main())
