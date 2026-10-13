# =====================================================================
# main.py: HET WEDSTRIJDPROGRAMMA (dit draait op de hub)
# =====================================================================
# Dit is het programma dat je start op de wedstrijd. Het toont een menu
# met letters (A, B, C, ...). Elke letter is een missie uit missies.py.
#   LINKS / RECHTS        : vorige / volgende missie kiezen
#   MIDDEN                : de gekozen missie starten
#   MIDDEN tijdens rijden : NOODSTOP
#   LINKS + RECHTS samen  : testmodus (een stukje van een missie testen)
#   letter V              : rijden met het toetsenbord (met stuur_robot.py)
# Uitleg voor beginners: zie docs/4-uitleg-code.md op GitHub
# =====================================================================

from supportcode import *
from missies import MISSIE_STAPPEN
# AANGEPAST (nieuw): het toetsenbord-rijden zit nu ook in het menu
from vrij_rijden import vrij_rijden

# Lijst van programma's
# AANGEPAST: vroeger stond hier PROGRAM_LIST = ['A', 'B', 'C', 'D', 'E'].
# Voegde je een missie toe in missies.py en vergat je ze hier, dan zat ze
# niet in het menu (of crashte het programma). Nu maken we de lijst
# automatisch uit de letters in MISSIE_STAPPEN. Een nieuwe missie toevoegen
# doe je dus enkel nog in missies.py.
# sorted() zet de letters in alfabetische volgorde: A, B, C, ...
MISSIE_LETTERS = sorted(MISSIE_STAPPEN)

# AANGEPAST (nieuw): na de missies staat in het menu nog de letter V van
# "vrij rijden". Kies je V en druk je MIDDEN, dan kan je de robot besturen
# met het toetsenbord (stuur_robot.py op de computer). Zo hoef je niet meer
# van programma te wisselen: main.py blijft gewoon op de hub staan.
# Een lijst + een lijst plakt ze aan elkaar: ['A', 'B'] + ['V'] = ['A', 'B', 'V']
VRIJ_RIJDEN = "V"
PROGRAM_LIST = MISSIE_LETTERS + [VRIJ_RIJDEN]
ACTIVEPROGRAM = 0

# Zet de standaard systeem-stopknop uit, wij regelen het nu zelf
HUB.system.set_stop_button(None)

# AANGEPAST (nieuw): toon welke versie van de code op de robot staat.
# VERSIE staat bovenaan supportcode.py. Vergelijk het met WIJZIGINGEN.md op GitHub.
print("githobotics code versie", VERSIE)


# =====================================================================
# MISSIES CONTROLEREN BIJ HET OPSTARTEN
# =====================================================================
# AANGEPAST (nieuw): voor het menu verschijnt, kijken we alle missies na op
# tikfouten (zie controleer_stappen() in supportcode.py).
# Is er een fout, dan:
#   - wordt het lampje ROOD
#   - toont het scherm de letter en het stapnummer, bv. "B 4"
#   - staat de uitleg in Pybricks Code (onderaan, bij de uitvoer)
# Een missie met een fout kan je niet starten. De andere missies wel, zodat
# je op de wedstrijd nooit vastzit door één foute missie.

# Een dictionary: letter van de missie -> lijst van fouten in die missie.
# Missies zonder fouten komen hier niet in.
FOUTE_MISSIES = {}
for letter in MISSIE_LETTERS:   # AANGEPAST: V is geen missie, die slaan we over
    fouten = controleer_stappen(MISSIE_STAPPEN[letter])
    if fouten:   # een lijst met iets erin telt als True
        FOUTE_MISSIES[letter] = fouten


def toon_fouten(letter):
    """Toont de fouten van één missie: op het scherm en in Pybricks Code."""
    HUB.light.on(Color.RED)
    HUB.speaker.beep(200, 500)
    for nummer, uitleg in FOUTE_MISSIES[letter]:
        print("FOUT in missie", letter, "stap", nummer, ":", uitleg)
        HUB.display.text(letter + " " + str(nummer))   # loopt over het scherm


# Bij het opstarten: toon meteen alle fouten
for letter in FOUTE_MISSIES:
    toon_fouten(letter)
if FOUTE_MISSIES:
    print("Verbeter deze fouten in missies.py. De andere missies werken wel.")


# =====================================================================
# TEST-MODUS
# =====================================================================
# Doel: nooit meer de hele missie vanaf het begin moeten laten rijden om één
# stap te controleren. Je kiest een STARTSTAP en een AANTAL stappen, de robot
# rijdt enkel dat stukje, en daarna kan je dat stukje meteen herhalen met één
# druk op de knop. Voor een simpele "straight"- of "turn"-stap kan je de
# waarde bovendien rechtstreeks op de hub bijstellen en meteen herproberen.

def kies_getal(kleur, minimum=0, maximum=None):
    """Hulpfunctie: laat de gebruiker met LEFT/RIGHT een getal kiezen, toont
    het op het scherm, en bevestigt met CENTER."""
    getal = minimum
    HUB.light.on(kleur)
    while True:
        HUB.display.number(getal)
        pressed = HUB.buttons.pressed()

        if Button.LEFT in pressed and Button.RIGHT in pressed:
            pass  # geen actie, dit is elders de combinatie om te annuleren
        elif Button.LEFT in pressed and getal > minimum:
            getal -= 1
            wait(200)
        elif Button.RIGHT in pressed and (maximum is None or getal < maximum):
            getal += 1
            wait(200)
        elif Button.CENTER in pressed:
            wacht_tot_losgelaten()
            return getal
        wait(10)


def wacht_op_keuze():
    """Na het uitvoeren van een teststukje: wacht op wat de gebruiker nu wil.
    - Kort op CENTER drukken: dezelfde reeks nog eens uitvoeren
    - LEFT+RIGHT tegelijk: een nieuwe startstap en aantal kiezen
    - RIGHT alleen: verder met het toetsenbord (AANGEPAST, nieuw)
    - CENTER 1,5 seconde ingedrukt houden: de testmodus verlaten
    Geeft 'herhaal', 'nieuw', 'toetsenbord' of 'stop' terug."""
    while True:
        pressed = HUB.buttons.pressed()
        if Button.CENTER in pressed:
            timer = StopWatch()
            while Button.CENTER in HUB.buttons.pressed():
                wait(10)
                if timer.time() > 1500:
                    return 'stop'
            return 'herhaal'
        elif Button.LEFT in pressed or Button.RIGHT in pressed:
            # AANGEPAST: twee knoppen druk je nooit op precies hetzelfde
            # moment in. Daarom onthouden we ALLE knoppen die we zien tot je
            # alles loslaat, en beslissen we pas dan.
            gezien = set()
            while HUB.buttons.pressed():
                for knop in HUB.buttons.pressed():
                    gezien.add(knop)
                wait(10)
            if Button.LEFT in gezien and Button.RIGHT in gezien:
                return 'nieuw'
            if Button.RIGHT in gezien:
                return 'toetsenbord'
            # enkel LEFT: daar doen we niets mee, gewoon verder wachten
        wait(10)


def test_enkele_waarde(stappen, index):
    """Enkel voor een 'straight'- of 'turn'-stap: laat je die ene waarde
    rechtstreeks op de hub bijstellen met LEFT/RIGHT (telkens 5 mm of graden),
    en meteen opnieuw testen met CENTER, zonder naar de computer te moeten.

    LET OP: dit past de code zelf niet aan. Onthoud het getal dat je op het
    einde op het scherm ziet en zet het nadien zelf over in missies.py.

    Geeft 'stop' terug als de testmodus helemaal verlaten moet worden,
    anders None (dan ga je terug naar het kiezen van een nieuwe reeks)."""
    STAP_GROOTTE = 5  # met hoeveel mm/graden je per druk op de knop verandert
    soort = stappen[index][0]
    waarde = stappen[index][1]

    HUB.light.on(Color.CYAN)
    while True:
        HUB.display.number(waarde)
        pressed = HUB.buttons.pressed()

        if Button.LEFT in pressed and Button.RIGHT in pressed:
            wacht_tot_losgelaten()
            return None  # terug naar het kiezen van een nieuwe startstap/aantal

        elif Button.LEFT in pressed:
            waarde -= STAP_GROOTTE
            wait(150)

        elif Button.RIGHT in pressed:
            waarde += STAP_GROOTTE
            wait(150)

        elif Button.CENTER in pressed:
            timer = StopWatch()
            while Button.CENTER in HUB.buttons.pressed():
                wait(10)
                if timer.time() > 1500:
                    return 'stop'  # lang ingedrukt: testmodus helemaal verlaten

            # Kort ingedrukt: voer deze ene stap uit met de huidige waarde
            HUB.light.on(Color.ORANGE)
            start_missie()  # nul de richting vanaf de positie waar de robot nu staat
            try:
                if soort == "straight":
                    safe_straight(waarde)
                else:
                    safe_turn(waarde)
                HUB.speaker.beep(600, 100)
            except MissionStop:
                print("Teststap gestopt door gebruiker.")
                DRIVE_BASE.stop()
                HUB.speaker.beep(200, 500)
                # AANGEPAST: wacht tot de stopknop los is, anders ziet de lus
                # hierboven die knop als een nieuwe druk en rijdt de robot
                # meteen opnieuw.
                wacht_tot_losgelaten()

            print("Stap", index, "(", soort, ") staat nu op:", waarde)
            HUB.light.on(Color.CYAN)

        wait(10)


def test_modus():
    """Hoofdlus van de testmodus. Wordt gestart met LEFT+RIGHT tegelijk vanuit
    het gewone menu."""
    actieve_letter = PROGRAM_LIST[ACTIVEPROGRAM]
    stappen = MISSIE_STAPPEN[actieve_letter]

    # AANGEPAST: een missie met een fout testen we niet
    if actieve_letter in FOUTE_MISSIES:
        toon_fouten(actieve_letter)
        return

    while True:
        start = kies_getal(Color.YELLOW, minimum=0, maximum=len(stappen) - 1)
        aantal = kies_getal(Color.VIOLET, minimum=1)
        eind = start + aantal

        # Bij precies 1 eenvoudige stap: laat de waarde live bijstellen
        if aantal == 1 and stappen[start][0] in ("straight", "turn"):
            resultaat = test_enkele_waarde(stappen, start)
            if resultaat == 'stop':
                return
            continue  # terug naar start/aantal kiezen

        # Anders: voer de gekozen reeks stappen uit, en laat herhalen
        while True:
            HUB.light.on(Color.ORANGE)
            try:
                start_missie()  # nul de richting vanaf de positie waar de robot nu staat
                voer_stappen_uit(stappen, start_bij=start, eind_stap=eind)
                HUB.speaker.beep(600, 100)
            except MissionStop:
                print("Teststukje gestopt door gebruiker.")
                DRIVE_BASE.stop()
                LEFT_ATTACHMENT.stop()
                RIGHT_ATTACHMENT.stop()
                HUB.speaker.beep(200, 500)
                wacht_tot_losgelaten()   # AANGEPAST: zie uitleg in test_enkele_waarde

            HUB.light.on(Color.GREEN)
            keuze = wacht_op_keuze()
            if keuze == 'stop':
                return
            elif keuze == 'nieuw':
                break  # terug naar buitenste lus: nieuwe start/aantal kiezen
            elif keuze == 'toetsenbord':
                # AANGEPAST (nieuw): de robot staat nu waar dit stuk van de
                # missie eindigt. Neem van hieruit het volgende stuk op met
                # het toetsenbord. vrij_rijden krijgt mee welke stappen de
                # robot al reed, zodat P (afspelen) alles kan afspelen en
                # de nieuwe stappen de juiste nummers krijgen.
                # stappen[start:eind] = de stappen van start tot (zonder) eind
                vrij_rijden(stappen[start:eind], actieve_letter, start)
                wacht_tot_losgelaten()
                return   # terug naar het menu
            # anders ('herhaal'): gewoon opnieuw door deze lus


# --- HOOFD PROGRAMMA LOOP ---
while True:
    HUB.system.set_stop_button(None)

    HUB.display.char(PROGRAM_LIST[ACTIVEPROGRAM])
    # AANGEPAST: rood lampje als deze missie een fout bevat, anders blauw
    # (en wit voor V, het rijden met het toetsenbord)
    if PROGRAM_LIST[ACTIVEPROGRAM] in FOUTE_MISSIES:
        HUB.light.on(Color.RED)
    elif PROGRAM_LIST[ACTIVEPROGRAM] == VRIJ_RIJDEN:
        HUB.light.on(Color.WHITE)
    else:
        HUB.light.on(Color.BLUE)

    pressed = HUB.buttons.pressed()

    # --- TEST-MODUS: beide knoppen tegelijk ---
    if Button.LEFT in pressed and Button.RIGHT in pressed:
        wacht_tot_losgelaten()
        # AANGEPAST: V is geen missie, die kan je niet testen
        if PROGRAM_LIST[ACTIVEPROGRAM] != VRIJ_RIJDEN:
            test_modus()

    # --- NAVIGATIE ---
    elif Button.LEFT in pressed:
        ACTIVEPROGRAM = prior_program(ACTIVEPROGRAM, PROGRAM_LIST)
        HUB.speaker.beep(200, 200)
        wait(250)  # Anti-bounce wachttijd

    elif Button.RIGHT in pressed:
        ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
        HUB.speaker.beep(500, 200)
        wait(250)

    # --- START VOLLEDIGE MISSIE ---
    elif Button.CENTER in pressed:
        # 1. Wacht tot je de knop LOSLAAT (belangrijk!)
        HUB.light.on(Color.ORANGE)
        wacht_tot_losgelaten()

        # AANGEPAST (nieuw): V = rijden met het toetsenbord
        if PROGRAM_LIST[ACTIVEPROGRAM] == VRIJ_RIJDEN:
            vrij_rijden()
            wacht_tot_losgelaten()   # de stopknop eerst loslaten
            continue

        # AANGEPAST: een missie met een fout starten we niet. We tonen de
        # fout opnieuw en gaan terug naar het menu.
        if PROGRAM_LIST[ACTIVEPROGRAM] in FOUTE_MISSIES:
            toon_fouten(PROGRAM_LIST[ACTIVEPROGRAM])
            continue   # continue = sla de rest over, begin de lus opnieuw

        # 2. Start het beveiligde blok
        try:
            start_missie()  # nult positie en richting van de robot (zie supportcode.py)

            actieve_letter = PROGRAM_LIST[ACTIVEPROGRAM]
            voer_stappen_uit(MISSIE_STAPPEN[actieve_letter])

            # --- EINDE VAN MISSIE (SUCCES) ---
            HUB.speaker.beep(600, 100)
            ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
            # AANGEPAST: na de laatste missie meteen terug naar A, niet naar V
            if PROGRAM_LIST[ACTIVEPROGRAM] == VRIJ_RIJDEN:
                ACTIVEPROGRAM = next_program(ACTIVEPROGRAM, PROGRAM_LIST)
            safe_wait(500)

        except MissionStop:
            # --- MISSIE AFGEBROKEN (FAIL) ---
            print("Missie gestopt door gebruiker.")
            DRIVE_BASE.stop()
            LEFT_ATTACHMENT.stop()
            RIGHT_ATTACHMENT.stop()
            HUB.speaker.beep(200, 500)  # Laag fout-geluidje
            wacht_tot_losgelaten()      # AANGEPAST: eerst de stopknop loslaten
            wait(500)  # Even wachten tegen per ongeluk dubbel klikken

    # Einde van while loop, ga terug naar het menu
    else:
        wait(10)
