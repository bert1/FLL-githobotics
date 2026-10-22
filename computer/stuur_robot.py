"""
stuur_robot.py: Bestuur de FLL-robot met je toetsenbord, via Bluetooth (BLE).

LET OP: dit programma draait op de COMPUTER (gewone Python), niet op de hub.
Het werkt samen met vrij_rijden.py, dat op de hub draait.
Uitleg voor beginners: zie docs/4-uitleg-code.md op GitHub

Vereist:
    pip install bleak pynput rich

AANGEPAST: op Windows hoef je niets te installeren. Download dan
stuur_robot.exe: dat is dit programma, samen met Python en alle
onderdelen in één bestand. Dubbelklik erop en het start.

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

AANGEPAST: het venster is nu een overzichtelijk "dashboard" met vaste
vakken (status, deze stap, de opname, de toetsen en meldingen), in plaats
van tekst die voorbijschuift. Daarvoor gebruiken we de bibliotheek "rich".

AANGEPAST (versie 2026-10-22): kopiëren is makkelijker. Druk C en de
stappen staan op het klembord, klaar om met CTRL+V in missies.py te
plakken. Na het stoppen gebeurt dat vanzelf. Elke opname wordt ook
bewaard in alle_opnames.txt, de nieuwste bovenaan, zonder tijdstip voor
elke regel en zonder stappen die je met BACKSPACE gewist hebt.

AANGEPAST: vroeger moest je vrij_rijden.py op de hub zetten en daarna
main.py terugzetten voor de wedstrijd. Dat hoeft niet meer: vrij rijden
zit in het menu van main.py (letter V). vrij_rijden.py zelf starten kan
ook nog altijd.
"""

import asyncio
import datetime
import subprocess
import sys
from collections import deque
from contextlib import suppress

# AANGEPAST: ontbreekt er een bibliotheek, dan zeggen we duidelijk wat je
# moet doen, in plaats van een lange Engelse foutmelding.
try:
    from bleak import BleakScanner, BleakClient
    from pynput import keyboard
    from rich.console import Console, Group
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.text import Text
except ImportError as fout:
    print("Er ontbreekt een onderdeel op deze computer:", fout.name)
    print("Typ in de terminal:   pip install bleak pynput rich")
    print("Of gebruik op Windows stuur_robot.exe, daar zit alles al in.")
    sys.exit(1)

# AANGEPAST (nieuw): "sys.frozen" bestaat enkel als dit programma als
# stuur_robot.exe draait (gemaakt met PyInstaller). Zo weten we of iemand
# erop dubbelklikte. Dan moet het venster op het einde blijven staan, anders
# verdwijnt het voor je de opname kan lezen.
IS_EXE = getattr(sys, "frozen", False)

# AANGEPAST (nieuw): met "stuur_robot.exe --controle" kijkt GitHub na of
# alle onderdelen in de .exe zitten, zonder met de hub te verbinden.
if "--controle" in sys.argv:
    # Het Bluetooth-deel voor Windows laadt bleak pas als het verbindt.
    # Daarom laden we het hier al eens, om te zien of het erin zit.
    if sys.platform == "win32":
        import bleak.backends.winrt.scanner
        import bleak.backends.winrt.client
    print("Alle onderdelen zijn aanwezig.")
    sys.exit(0)

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"

# Pas dit aan als je de hub in Pybricks Code een andere naam gaf
HUB_NAME = "githo botic"

# AANGEPAST (nieuw): in stuur_robot.exe kan je HUB_NAME niet aanpassen.
# Zet daarom een bestand hubnaam.txt in dezelfde map, met op de eerste
# regel de naam van jullie hub. Staat dat bestand er, dan gebruiken we die
# naam in plaats van de naam hierboven.
with suppress(OSError):
    with open("hubnaam.txt", encoding="utf-8") as bestand:
        HUB_NAME = bestand.readline().strip() or HUB_NAME

# AANGEPAST (nieuw): hier komen de opgenomen stappen, klaar om te plakken
OPNAMEBESTAND = "opname.txt"
# AANGEPAST (nieuw): vroeger kwam alles in rijlog.txt, met een tijdstip voor
# elke regel, ook de stappen die je daarna wiste. Moeilijk om te kopiëren!
# Nu komt hier elke AFGEWERKTE opname, zoals ze op het einde was. De
# nieuwste staat bovenaan. rijlog.txt mag je weggooien.
ARCHIEFBESTAND = "alle_opnames.txt"

# AANGEPAST (nieuw): moet hetzelfde getal zijn als PROTOCOL in vrij_rijden.py
PROTOCOL = 3

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
# BACKSPACE   : laatste stap wissen, de robot rijdt terug
# R           : opname wissen en opnieuw beginnen (nulpunt hier)
# P           : alles afspelen op wedstrijdsnelheid (zet de robot eerst
#               terug op de startplek!)
# ENTER       : de opname groot tonen (nog eens ENTER: terug klein)
# C           : de stappen kopiëren, plakken doe je met CTRL+V
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

# AANGEPAST (nieuw): letters die maar ÉÉN keer iets doen als je ze indrukt
EENMALIGE_TOETSEN = {
    "p": "afspelen",
}

# AANGEPAST (nieuw): de cijfertoetsen voor de stapgrootte. Op een AZERTY-
# toetsenbord geven de cijfers bovenaan zonder SHIFT de tekens & é " ,
# daarom staan die er ook bij.
STAPGROOTTE_TOETSEN = {
    "1": "1", "&": "1",
    "2": "2", "é": "2",
    "3": "3", '"': "3",
}
# Wat elke stapgrootte betekent, om op het scherm te tonen. Pas je
# STAPGROOTTES aan in vrij_rijden.py, pas dan ook deze tekst aan.
STAPGROOTTE_UITLEG = {
    "1": "fijn: 1 mm, 1°",
    "2": "normaal: 5 mm, 1°",
    "3": "grof: 20 mm, 5°",
}

ingedrukte_toetsen = set()  # bevat de ACTIES (bv. "vooruit"), niet de letters
# AANGEPAST (nieuw): acties die maar ÉÉN keer verstuurd worden (bv. SPATIE),
# ook als je de toets heel kort aantikt of lang vasthoudt
eenmalige_acties = set()
# AANGEPAST (nieuw): met deze letter kopieer je de stappen naar het klembord
KOPIEER_TOETS = "c"

# Toetsen die nu fysiek ingedrukt zijn. Houd je een toets lang vast, dan
# stuurt de computer die toets steeds opnieuw ("autorepeat"). Zo herkennen
# we dat en tellen we het maar één keer.
al_ingedrukt = set()
stapgrootte = "2"

# AANGEPAST (nieuw): een kopie van de opname op de hub
opname = []                     # de stappen als tekst, bv. '("straight", 412),'
eerste_nummer = 0               # het stapnummer van de eerste stap
vooraf_uitleg = ""              # uit de testmodus: welke missie de robot al reed

# AANGEPAST (nieuw): alles wat op het scherm staat. De functies onderaan
# (maak_scherm en zijn helpers) tekenen het scherm 10 keer per seconde
# opnieuw met wat hier staat.
scherm = {
    "fase": "Zoeken naar de hub...",   # wat er nu gebeurt
    "fase_kleur": "yellow",            # kleur van het bolletje ervoor
    "hub_versie": "",                  # versie van de code op de hub
    "stapmodus": False,
    "afstand": 0,                      # metingen van de HUIDIGE stap
    "hoek": 0,
    "links": 0,
    "rechts": 0,
    "opname_groot": False,             # ENTER: opname over het hele scherm
}
# De laatste meldingen. Een deque met maxlen=6 onthoudt er hoogstens 6:
# komt er een nieuwe bij, dan valt de oudste eraf.
meldingen = deque(maxlen=6)

console = Console()


def toon(tekst, stijl=""):
    """AANGEPAST: zet een melding onderaan het scherm, met het tijdstip.
    stijl is de kleur, bv. "green" of "bold red". Leeg = gewone tekst."""
    tijd = datetime.datetime.now().strftime("%H:%M:%S")
    meldingen.append((tijd, tekst, stijl))


def zet_fase(tekst, kleur):
    """AANGEPAST (nieuw): wat er nu gebeurt, bovenaan het scherm."""
    scherm["fase"] = tekst
    scherm["fase_kleur"] = kleur


def metingen_op_nul():
    """Na een nieuwe stap begint de huidige stap weer bij 0."""
    for naam in ("afstand", "hoek", "links", "rechts"):
        scherm[naam] = 0


def stappen_als_tekst():
    """AANGEPAST (nieuw): ENKEL de stappen, zonder iets erboven of erond.
    Precies wat je in missies.py plakt, bv.
        ("straight", 412),                              # stap 0"""
    regels = []
    for i, stap in enumerate(opname):
        regels.append("    " + stap.ljust(48) + "# stap " + str(eerste_nummer + i))
    return "\n".join(regels) + "\n"


def opname_als_tekst():
    """Maakt de tekst voor opname.txt: de stappen met hun nummer."""
    tijd = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    regels = [
        "# Opname van stuur_robot.py (" + tijd + ")",
        "# Kopieer de stappen naar je missie in missies.py, boven de regel",
        '# ("call", stop_attachments). Het nummer achter # is het stapnummer.',
    ]
    if vooraf_uitleg:
        regels.append(vooraf_uitleg)
    if opname:
        regels.append(stappen_als_tekst().rstrip())   # AANGEPAST: zie hierboven
    else:
        regels.append("# (nog geen stappen)")
    return "\n".join(regels) + "\n"


def schrijf_opname():
    """Zet de opname in opname.txt. Dit gebeurt na ELKE wijziging, zodat
    het bestand altijd klopt, ook als het programma plots stopt."""
    with open(OPNAMEBESTAND, "w", encoding="utf-8") as bestand:
        bestand.write(opname_als_tekst())


def bewaar_in_archief():
    """AANGEPAST (nieuw): zet de opname BOVENAAN in alle_opnames.txt.
    Dit gebeurt als je een nieuwe opname begint (R, of opnieuw V op de hub)
    en als je stopt. Zo verlies je nooit een oude opname, en staat de
    nieuwste altijd bovenaan. Gewiste stappen (BACKSPACE) staan er niet in."""
    if not opname:
        return
    tijd = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    blok = "# ===== Opname van " + tijd + " (" + str(len(opname)) + " stappen) =====\n"
    if vooraf_uitleg:
        blok += vooraf_uitleg + "\n"
    blok += stappen_als_tekst() + "\n"
    # Eerst lezen wat er al in staat (bestaat het bestand nog niet, dan is
    # dat leeg), en dan alles opnieuw schrijven met het nieuwe blok bovenaan.
    oud = ""
    with suppress(OSError):
        with open(ARCHIEFBESTAND, encoding="utf-8") as bestand:
            oud = bestand.read()
    with open(ARCHIEFBESTAND, "w", encoding="utf-8") as bestand:
        bestand.write(blok + oud)


def kopieer_naar_klembord(tekst):
    """AANGEPAST (nieuw): zet tekst op het klembord, zoals CTRL+C.
    Elk besturingssysteem heeft daar een eigen klein programma voor:
    Windows "clip", Mac "pbcopy", Linux "xclip". subprocess.run() start
    dat programma en geeft het de tekst. Geeft True terug als het lukte."""
    try:
        if sys.platform == "win32":
            # clip wil de tekst in "utf-16", anders worden letters als é raar
            subprocess.run("clip", input=tekst.encode("utf-16"), check=True)
        elif sys.platform == "darwin":
            subprocess.run("pbcopy", input=tekst.encode("utf-8"), check=True)
        else:
            subprocess.run(["xclip", "-selection", "clipboard"],
                           input=tekst.encode("utf-8"), check=True)
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


def kopieer_opname():
    """AANGEPAST (nieuw): de stappen naar het klembord (toets C)."""
    if not opname:
        toon("Er zijn nog geen stappen om te kopiëren.", "yellow")
        return False
    if kopieer_naar_klembord(stappen_als_tekst()):
        toon("%d stappen gekopieerd. Plak ze met CTRL+V in missies.py." % len(opname),
             "bold green")
        return True
    toon("Kopiëren lukt niet op deze computer. Open " + OPNAMEBESTAND + ".", "bold red")
    return False


def verwerk_hub_regel(tekst):
    """AANGEPAST: leest een regel van de hub en past het scherm aan.
    Regels die beginnen met NIEUW, STAP of WEG houden de opname bij,
    "nu ..." geeft de metingen van de huidige stap."""
    global eerste_nummer, vooraf_uitleg
    delen = tekst.split(" ", 2)    # hoogstens in 3 stukken knippen

    if delen[0] == "nu":
        # bv. "nu afstand=412 hoek=-3 links=0 rechts=0"
        for deel in tekst.split()[1:]:
            naam, _, waarde = deel.partition("=")
            if naam in scherm:
                with suppress(ValueError):
                    scherm[naam] = int(waarde)
        return

    if delen[0] == "NIEUW" and len(delen) >= 2:
        # "NIEUW 0" of, uit de testmodus, "NIEUW 5 B 0": nieuwe stappen
        # vanaf nummer 5, nadat de robot missie B vanaf stap 0 reed
        stukken = tekst.split()
        # AANGEPAST: eerst de vorige opname bewaren in alle_opnames.txt
        if opname:
            bewaar_in_archief()
            toon("Vorige opname bewaard in " + ARCHIEFBESTAND + ".", "dim")
        eerste_nummer = int(stukken[1])
        if len(stukken) >= 4:
            vooraf_uitleg = ("# De robot reed eerst MISSIE_%s van stap %s tot en met stap %d.\n"
                             "# Plak deze stappen in MISSIE_%s, net na stap %d."
                             % (stukken[2], stukken[3], eerste_nummer - 1,
                                stukken[2], eerste_nummer - 1))
            toon("Verder na stap %d van MISSIE_%s." % (eerste_nummer - 1, stukken[2]), "cyan")
        else:
            vooraf_uitleg = ""
            toon("Nieuwe opname gestart.", "cyan")
        opname.clear()
        metingen_op_nul()
        schrijf_opname()
        return

    if delen[0] == "STAP" and len(delen) == 3:
        plaats = int(delen[1]) - eerste_nummer
        del opname[plaats:]      # alles vanaf deze plaats weg (meestal niets)
        opname.append(delen[2])
        metingen_op_nul()
        schrijf_opname()
        toon("Stap " + delen[1] + " opgenomen: " + delen[2], "green")
        return

    if delen[0] == "WEG" and len(delen) >= 2:
        plaats = int(delen[1]) - eerste_nummer
        del opname[plaats:]
        metingen_op_nul()
        schrijf_opname()
        toon("Stap " + delen[1] + " gewist, de robot reed terug.", "yellow")
        return

    if delen[0] == "KLAAR":
        return     # de hub heeft de stap afgesloten, er is niets te tonen

    # --- Gewone berichten van de hub ---
    if tekst.startswith("githobotics code versie"):
        scherm["hub_versie"] = tekst.split()[-1]
    elif tekst.startswith("Stapmodus"):
        scherm["stapmodus"] = tekst.endswith("AAN")
    elif tekst.startswith("Stapgrootte"):
        pass       # dat staat al in het vak "Instellingen"
    elif tekst.startswith("Vrij rijden gestart"):
        zet_fase("Rijden en opnemen", "green")
    elif tekst.startswith("Afspelen op wedstrijdsnelheid"):
        zet_fase("Afspelen op wedstrijdsnelheid (MIDDEN op de hub = stoppen)", "magenta")
        toon("Afspelen gestart.", "magenta")
    elif tekst.startswith("Afspelen"):
        zet_fase("Rijden en opnemen", "green")
        toon(tekst, "magenta")
    elif tekst.startswith("Geen verbinding") or tekst.startswith("FOUT"):
        toon(tekst, "bold red")
    elif tekst.startswith("Gestopt"):
        toon(tekst, "yellow")
    else:
        toon("Hub: " + tekst, "dim")


def on_press(key):
    global stapgrootte

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
        # AANGEPAST: ENTER wisselt tussen de opname klein en groot. Dit
        # gebeurt enkel op de computer, de hub merkt er niets van.
        scherm["opname_groot"] = not scherm["opname_groot"]
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
    if naam == KOPIEER_TOETS:
        # AANGEPAST (nieuw): kopiëren gebeurt enkel op de computer
        kopieer_opname()
        return
    if naam in EENMALIGE_TOETSEN:
        eenmalige_acties.add(EENMALIGE_TOETSEN[naam])
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
    """Bouwt het commando voor de hub: 15 tekens '1' of '0', dan de
    stapgrootte ("1", "2" of "3") en een Enter-teken (\\n) op het einde.
    De volgorde moet exact overeenkomen met vrij_rijden.py op de hub."""
    # AANGEPAST: de eenmalige acties worden één keer meegestuurd en daarna
    # meteen gewist. De hub ziet ze zo als één tik.
    toetsen = set(ingedrukte_toetsen)   # een kopie, het origineel blijft hetzelfde
    toetsen.update(eenmalige_acties)    # update() voegt een hele verzameling toe
    eenmalige_acties.clear()

    volgorde = ("vooruit", "links", "achteruit", "rechts", "nulpunt", "stoppen",
                "links_att_plus", "links_att_min", "rechts_att_plus", "rechts_att_min",
                "precisie", "stapmodus", "stap_klaar", "ongedaan", "afspelen")
    bits = "".join("1" if t in toetsen else "0" for t in volgorde)
    return (bits + stapgrootte + "\n").encode()


# =====================================================================
# HET SCHERM TEKENEN
# =====================================================================
# AANGEPAST (nieuw): het scherm bestaat uit vakken ("panelen"):
#
#   +--------------------------------------------------+
#   | KOP: wat gebeurt er nu? verbonden? welke versie?   |
#   +---------------+----------------------------------+
#   | DEZE STAP     | OPNAME                           |
#   | INSTELLINGEN  | (de stappen voor missies.py)     |
#   +---------------+----------------------------------+
#   | TOETSEN                                          |
#   +--------------------------------------------------+
#   | MELDINGEN                                        |
#   +--------------------------------------------------+
#
# Elke functie hieronder maakt één vak. maak_scherm() zet ze samen.
# De bibliotheek "rich" tekent alles 10 keer per seconde opnieuw.

def toets(letters):
    """Tekent een toets als een "knopje": zwarte letters op een licht vlak.
    Enkel de letters krijgen de kleur, niet de lege ruimte ernaast."""
    tekst = Text(justify="right")
    tekst.append(" " + letters + " ", style="bold black on grey85")
    return tekst


def maak_kop(toon_melding):
    """Bovenaan: wat gebeurt er nu? Is 'toon_melding' True (klein venster,
    zonder vak Meldingen), dan staat de laatste melding hier."""
    regel = Text(no_wrap=True, overflow="ellipsis")
    regel.append("● ", style=scherm["fase_kleur"])
    regel.append(scherm["fase"], style="bold")
    info = Text(style="dim", no_wrap=True, overflow="ellipsis")
    if toon_melding and meldingen:
        tijd, melding, stijl = meldingen[-1]    # [-1] = het laatste element
        info.append(melding, style=stijl)
    else:
        info.append("hub: " + HUB_NAME)
        if scherm["hub_versie"]:
            info.append("   versie " + scherm["hub_versie"])
        info.append("   opname: " + OPNAMEBESTAND)
    if scherm["opname_groot"]:
        info.append("   ENTER = terug", style="bold yellow")
    return Panel(Group(regel, info),
                 title="[bold]githobotics[/]  rijden met het toetsenbord",
                 title_align="left", border_style="blue")


def maak_metingen():
    """Hoeveel is de robot bewogen in de stap die nu loopt?"""
    tabel = Table.grid(padding=(0, 2))
    tabel.add_column(style="dim")
    tabel.add_column(justify="right", style="bold")
    tabel.add_column(style="dim")
    tabel.add_row("Afstand", str(scherm["afstand"]), "mm")
    tabel.add_row("Hoek", str(scherm["hoek"]), "graden")
    tabel.add_row("Linker arm", str(scherm["links"]), "graden")
    tabel.add_row("Rechter arm", str(scherm["rechts"]), "graden")
    nummer = eerste_nummer + len(opname)
    return Panel(tabel, title="Deze stap (nr. %d)" % nummer,
                 title_align="left", border_style="cyan")


def maak_instellingen():
    tabel = Table.grid(padding=(0, 2))
    tabel.add_column(style="dim")
    tabel.add_column()
    if scherm["stapmodus"]:
        tabel.add_row("Modus", Text("STAPMODUS", style="bold yellow"))
    else:
        tabel.add_row("Modus", "gewoon rijden")
    if "precisie" in ingedrukte_toetsen:
        tabel.add_row("Snelheid", Text("extra traag", style="bold yellow"))
    else:
        tabel.add_row("Snelheid", "normaal")
    tabel.add_row("Stapgrootte", stapgrootte + " (" + STAPGROOTTE_UITLEG[stapgrootte] + ")")
    return Panel(tabel, title="Instellingen", title_align="left", border_style="cyan")


def kleur_stap(stap):
    """Kleurt een stap zoals in een code-editor (tekst, getallen, ...)."""
    tekst = Syntax(stap, "python", background_color="default").highlight(stap)
    tekst.rstrip()     # de Enter op het einde weghalen
    return tekst


def maak_opname(hoogte):
    """De opgenomen stappen. 'hoogte' is hoeveel regels het vak hoog is.
    Passen niet alle stappen, dan tonen we de laatste."""
    # Er gaan 3 regels af: de rand boven en onder, en de regel met de titels
    plaats = max(1, hoogte - 3)
    if len(opname) > plaats:
        plaats -= 1    # één regel voor "... nog x stappen hierboven"
    tabel = Table(box=None, expand=True, show_header=True, header_style="dim")
    tabel.add_column("stap", justify="right", width=5)
    tabel.add_column("code voor missies.py", ratio=1, no_wrap=True, overflow="ellipsis")

    begin = max(0, len(opname) - plaats)
    if begin > 0:
        tabel.add_row("", Text("... nog %d stap(pen) hierboven" % begin,
                               style="dim", no_wrap=True, overflow="ellipsis"))
    for i in range(begin, len(opname)):
        tekst = kleur_stap(opname[i])
        nummer = Text(str(eerste_nummer + i), style="dim")
        if i == len(opname) - 1:
            # de nieuwste stap valt op
            nummer = Text(str(eerste_nummer + i), style="bold green")
            tekst.append("   < nieuw", style="bold green")
        tabel.add_row(nummer, tekst)
    if not opname:
        tabel.add_row("", Text("Nog geen stappen. Rij met Z Q S D!", style="dim italic"))

    titel = "Opname (%d stappen)" % len(opname)
    onder = ""
    if vooraf_uitleg:
        # bv. "Plak deze stappen in MISSIE_B, net na stap 4."
        onder = vooraf_uitleg.split("\n")[-1].lstrip("# ")
    return Panel(tabel, title=titel, title_align="left", subtitle=onder,
                 subtitle_align="left", border_style="green")


def maak_toetsen(kort):
    """Een spiekbriefje met alle toetsen, in drie kolommen.
    kort = True: kortere uitleg, voor een smal venster."""
    tabel = Table.grid(padding=(0, 1), expand=True)
    for _ in range(3):
        tabel.add_column(no_wrap=True, justify="right")
        tabel.add_column(ratio=1, no_wrap=True, overflow="ellipsis")
    if kort:
        rijen = [
            ("Z S", "rijden", "SPATIE", "stap klaar", "M", "stapmodus"),
            ("Q D", "draaien", "BACKSPACE", "stap terug", "1 2 3", "stapgrootte"),
            ("Z+Q", "bocht", "P", "afspelen", "ENTER", "opname groot"),
            ("I K", "linker arm", "R", "nieuwe opname", "ESC", "stoppen"),
            ("O L", "rechter arm", "C", "kopiëren", "MIDDEN", "noodstop hub"),
            ("SHIFT", "extra traag", "", "", "", ""),
        ]
    else:
        rijen = [
            ("Z S", "vooruit / achteruit", "SPATIE", "stap afsluiten", "M", "stapmodus aan/uit"),
            ("Q D", "draaien", "BACKSPACE", "laatste stap terug", "1 2 3", "stapgrootte"),
            ("Z+Q", "bocht", "P", "afspelen (wedstrijd)", "ENTER", "opname groot/klein"),
            ("I K", "linker arm", "R", "nieuwe opname", "ESC", "stoppen"),
            ("O L", "rechter arm", "C", "kopiëren (CTRL+V)", "MIDDEN", "noodstop (op de hub)"),
            ("SHIFT", "extra traag", "", "", "", ""),
        ]
    for t1, u1, t2, u2, t3, u3 in rijen:
        tabel.add_row(toets(t1) if t1 else "", u1,
                      toets(t2) if t2 else "", u2,
                      toets(t3) if t3 else "", u3)
    return Panel(tabel, title="Toetsen  [dim](rijden | opnemen | andere)[/]",
                 title_align="left", border_style="bright_black")


def maak_meldingen(hoogte):
    """De nieuwste meldingen, zoveel als er passen in een vak van 'hoogte'
    regels (min 2 voor de rand boven en onder)."""
    tekst = Text()
    # list(...)[-3:] = de laatste 3 elementen van de lijst
    for tijd, melding, stijl in list(meldingen)[-(hoogte - 2):]:
        tekst.append(tijd + "  ", style="dim")
        tekst.append(melding + "\n", style=stijl)
    tekst.rstrip()
    return Panel(tekst, title="Meldingen", title_align="left", border_style="bright_black")


def maak_scherm():
    """Zet alle vakken samen tot één scherm. Hoe groot elk vak wordt, hangt
    af van hoe groot het terminalvenster is."""
    breedte = console.size.width
    hoogte = console.size.height
    kop_hoogte = 4
    toetsen_hoogte = 8
    # Het vak Meldingen: groot in een hoog venster, klein in een gewoon
    # venster, en weg in een laag venster (dan staat de laatste melding
    # in de kop).
    if hoogte >= 34:
        meldingen_hoogte = 8
    elif hoogte >= 27:
        meldingen_hoogte = 5
    else:
        meldingen_hoogte = 0

    scherm_layout = Layout()
    if scherm["opname_groot"]:
        # ENTER: de opname krijgt het hele scherm onder de kop
        scherm_layout.split_column(
            Layout(maak_kop(True), size=kop_hoogte),
            Layout(maak_opname(hoogte - kop_hoogte)),
        )
        return scherm_layout

    midden_hoogte = hoogte - kop_hoogte - toetsen_hoogte - meldingen_hoogte
    vakken = [
        Layout(maak_kop(meldingen_hoogte == 0), size=kop_hoogte),
        Layout(name="midden", size=midden_hoogte),
        Layout(maak_toetsen(breedte < 110), size=toetsen_hoogte),
    ]
    if meldingen_hoogte > 0:
        vakken.append(Layout(maak_meldingen(meldingen_hoogte), size=meldingen_hoogte))
    scherm_layout.split_column(*vakken)   # * = elk vak uit de lijst apart meegeven

    # Links: de metingen, en de instellingen als er plaats genoeg is
    if midden_hoogte >= 11:
        links = Group(maak_metingen(), maak_instellingen())
    else:
        links = maak_metingen()
    scherm_layout["midden"].split_row(
        Layout(links, size=38),
        Layout(maak_opname(midden_hoogte)),
    )
    return scherm_layout


def gooi_getypte_toetsen_weg():
    """AANGEPAST (nieuw): alles wat je tijdens het rijden typte (zzzzqqq...)
    staat ook in de terminal. Dat wissen we, anders probeert de terminal
    het na het stoppen uit te voeren als een commando."""
    try:
        import msvcrt          # bestaat enkel op Windows
        while msvcrt.kbhit():
            msvcrt.getwch()
    except ImportError:
        with suppress(Exception):
            import termios     # bestaat enkel op Mac en Linux
            termios.tcflush(sys.stdin, termios.TCIFLUSH)


# =====================================================================
# HET HOOFDPROGRAMMA
# =====================================================================

async def main():
    main_task = asyncio.current_task()

    def handle_disconnect(_):
        zet_fase("Verbinding met de hub verbroken", "red")
        toon("Verbinding met de hub verbroken.", "bold red")
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

        # 2) Enkel volledige regels (tot aan een Enter) verwerken
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
                    einde_event.clear()
                    zet_fase("Rijden en opnemen", "green")
                else:
                    zet_fase("Deze stuur_robot.py past niet bij de code op de hub", "red")
                    toon("Download de nieuwste stuur_robot.py en de nieuwste code voor de hub.",
                         "bold red")
                continue
            if regel.startswith("Klaar om te rijden"):
                # zo begon de OUDE vrij_rijden.py
                zet_fase("De hub heeft een oude vrij_rijden.py", "red")
                toon("Zet de nieuwste code op de hub.", "bold red")
                continue
            if regel == "EINDE":
                einde_event.set()
                zet_fase("De hub staat in het menu. Kies V en druk MIDDEN om verder te rijden.",
                         "yellow")
                continue

            verwerk_hub_regel(regel)

    toon("Zorg dat Pybricks Code losgekoppeld is van de hub.")

    # AANGEPAST: valt de verbinding weg, dan stopt het programma (zie
    # handle_disconnect). Met try/except vangen we dat op, zodat je daarna
    # toch nog je opname te zien krijgt.
    verbroken = False
    gevonden = True
    try:
        await rijden_met_dashboard(handle_rx, handle_disconnect, ready_event,
                                   protocol_ok, einde_event)
    except LookupError:
        gevonden = False
    except asyncio.CancelledError:
        verbroken = True

    gooi_getypte_toetsen_weg()

    if not gevonden:
        console.print(Panel(
            "Kon de hub [bold]" + HUB_NAME + "[/] niet vinden.\n\n"
            "- Staat Bluetooth aan op je computer?\n"
            "- Is Pybricks Code losgekoppeld van de hub?\n"
            "- Staat de hub aan?\n"
            "- Klopt de naam [bold]" + HUB_NAME + "[/] met de naam in Pybricks Code?\n"
            "  Zo niet: zet een bestand hubnaam.txt met de juiste naam in deze map.",
            title="Niet gevonden", title_align="left", border_style="red"))
        return

    # AANGEPAST: na het stoppen de opname nog eens tonen in de gewone
    # terminal. Vroeger stond ze in een kader: wie ze selecteerde, kopieerde
    # ook de randen mee. Nu staan de stappen er gewoon, zonder kader en
    # zonder tijdstip, en staan ze meteen ook op het klembord.
    bewaar_in_archief()
    console.print()
    console.rule("[bold green]Opname[/]", align="left", style="green")
    if vooraf_uitleg:
        print(vooraf_uitleg)
    if opname:
        print(stappen_als_tekst(), end="")   # gewone print: geen kleuren, geen kader
    else:
        print("(geen stappen opgenomen)")
    console.rule(style="green")
    if opname and kopieer_naar_klembord(stappen_als_tekst()):
        console.print("[bold green]De stappen staan al op het klembord.[/] "
                      "Plak ze in missies.py met CTRL+V (op een Mac: CMD+V).")
    elif opname:
        console.print("Kopieer de stappen hierboven, of open " + OPNAMEBESTAND + ".")
    console.print("[dim]Ook bewaard in " + OPNAMEBESTAND + " en, met alle vorige opnames, in "
                  + ARCHIEFBESTAND + ".[/]")
    if verbroken:
        console.print("[bold red]De verbinding met de hub viel weg.[/] "
                      "Wat al opgenomen was, staat hierboven.")


async def rijden_met_dashboard(handle_rx, handle_disconnect, ready_event,
                               protocol_ok, einde_event):
    """AANGEPAST (nieuw): verbinden met de hub en rijden, terwijl het
    dashboard op het scherm staat. Geeft een LookupError als de hub niet
    gevonden wordt."""
    # Vanaf hier tekent "Live" het scherm, 10 keer per seconde.
    # screen=True: het dashboard krijgt het hele terminalvenster. Als het
    # programma stopt, komt je gewone terminal terug.
    with Live(get_renderable=maak_scherm, screen=True, refresh_per_second=10,
              console=console):
        device = await BleakScanner.find_device_by_name(HUB_NAME)
        if device is None:
            raise LookupError("hub niet gevonden")
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

            zet_fase("Verbonden! Start main.py met de knop op de hub, kies V en druk MIDDEN.",
                     "yellow")
            toon("Verbonden met " + HUB_NAME + ".", "green")

            while "stoppen" not in ingedrukte_toetsen:
                await send(maak_commando())
                await asyncio.sleep(0.02)

            zet_fase("Stoppen...", "yellow")
            await send(maak_commando())  # laatste commando (met stoppen=1) sluit de hub-lus af
            luisteraar.stop()
            # AANGEPAST: even wachten tot de hub de laatste stap doorstuurde
            with suppress(asyncio.TimeoutError):
                await asyncio.wait_for(einde_event.wait(), 3)


if __name__ == "__main__":
    with suppress(asyncio.CancelledError, KeyboardInterrupt):
        asyncio.run(main())
    # AANGEPAST (nieuw): wie op stuur_robot.exe dubbelklikte, krijgt een
    # venster dat vanzelf sluit als het programma stopt. Daarom wachten we
    # hier op ENTER, zodat je eerst nog alles rustig kan lezen.
    if IS_EXE:
        with suppress(EOFError, KeyboardInterrupt):
            input("\nDruk op ENTER om dit venster te sluiten.")
