# =====================================================================
# vrij_rijden.py: DE ROBOT BESTUREN MET HET TOETSENBORD (dit draait op de hub)
# =====================================================================
# Dit programma luistert naar commando's die stuur_robot.py vanaf de
# computer stuurt, en laat de robot rijden zolang je een toets indrukt.
#
# AANGEPAST: het programma NEEMT NU OOK OP. Elke beweging die je maakt
# (rechtdoor, draaien, een bocht, een attachment) wordt automatisch een
# stap voor missies.py. Begin je aan een ANDERE soort beweging, dan wordt
# de vorige stap afgesloten. stuur_robot.py schrijft alle stappen in het
# bestand opname.txt op de computer, klaar om te plakken.
#
# AANGEPAST: je kan dit programma op twee manieren starten:
#   1. vanuit het menu van main.py: kies de letter V (zo hoef je niet
#      meer van programma te wisselen, main.py blijft op de hub staan)
#   2. zoals vroeger: vrij_rijden.py zelf op de hub laden en starten
#   3. AANGEPAST (nieuw): vanuit de testmodus van main.py, nadat de robot
#      een stuk van een missie gereden heeft. Zo neem je het VOLGENDE
#      stuk van die missie op, vanaf de plek waar de missie eindigt.
# AANGEPAST (nieuw): met P speel je de opname af op wedstrijdsnelheid.
# Uitleg voor beginners: zie docs/4-uitleg-code.md op GitHub
# =====================================================================

import math

from supportcode import (DRIVE_BASE, HUB, LEFT_ATTACHMENT, RIGHT_ATTACHMENT,
                         MissionStop, safe_straight, safe_turn, safe_curve,
                         safe_run_angle, start_missie, voer_stappen_uit,
                         wacht_tot_losgelaten)
from pybricks.parameters import Button, Color
from pybricks.tools import wait, StopWatch

# Standaard MicroPython-modules voor het lezen van inkomende data
from usys import stdin, stdout
from uselect import poll

# =====================================================================
# INSTELLINGEN (pas hier aan, nergens anders)
# =====================================================================
# Gewone snelheid (Z/S ingedrukt houden)
RIJSNELHEID = 120                   # mm per seconde
DRAAISNELHEID = 45                  # graden per seconde
ATTACHMENT_SNELHEID = 150           # graden per seconde

# Met SHIFT ingedrukt: nog trager, voor de laatste millimeters
PRECIEZE_RIJSNELHEID = 40
PRECIEZE_DRAAISNELHEID = 15
PRECIEZE_ATTACHMENT_SNELHEID = 40

# STAPMODUS (aan/uit met M): elke tik op een toets = één exacte, kleine stap
# AANGEPAST: vroeger was er maar één stapgrootte. Nu kies je er een met de
# cijfertoetsen 1, 2 en 3 op het toetsenbord, zonder iets aan te passen.
# Per keuze: (mm per tik voor Z/S, graden per tik voor Q/D,
#             motorgraden per tik voor de attachments)
STAPGROOTTES = {
    "1": (1, 1, 1),       # heel fijn
    "2": (5, 1, 5),       # normaal (zo begint het programma)
    "3": (20, 5, 20),     # grof, om snel dichterbij te komen
}

# AANGEPAST (nieuw): instellingen voor het OPNEMEN van stappen
# Welke snelheid komt er in een opgenomen attachment-stap, bv.
# ("run_angle", LEFT_ATTACHMENT, 200, 90)? (graden per seconde)
ATTACHMENT_SNELHEID_IN_MISSIE = 200
# Kleinere bewegingen dan dit zijn ruis en worden geen stap
MIN_AFSTAND = 3          # mm
MIN_HOEK = 1             # graden
MIN_ATTACHMENT = 2       # motorgraden
# Reed de robot vooruit EN draaide hij tegelijk (Z en Q samen), dan wordt
# het een bocht ("curve"), maar enkel als beide groot genoeg zijn
BOCHT_MIN_AFSTAND = 20   # mm
BOCHT_MIN_HOEK = 5       # graden

# Welke regeling houdt de robot recht?
# True  = onze eigen PID hieronder (instelbaar met KP, KI, KD)
# False = de ingebouwde gyroregeling van Pybricks (rekent sneller, binnenin de hub)
# Probeer beide eens op de mat en kies wat het rechtst rijdt.
GEBRUIK_EIGEN_PID = True

# PID-regeling: houdt de robot recht terwijl hij vooruit/achteruit rijdt
KP = 2.0      # P: hoe hard corrigeren we bij een fout van 1 graad
KI = 1.0      # I: wegwerken van een kleine fout die blijft hangen
KD = 0.1      # D: afremmen van de correctie zodat de robot niet gaat slingeren
DODE_ZONE = 0.3       # afwijkingen kleiner dan dit (graden) negeren: dat is ruis
MAX_CORRECTIE = 20    # nooit harder bijsturen dan 20 graden per seconde
MAX_INTEGRAAL = 10    # voorkomt dat het I-deel ongecontroleerd groeit

LUS_TIJD = 10         # ms: de hub rekent de PID 100 keer per seconde

VEILIGHEID_TIMEOUT = 500   # ms: stop de motoren als er dit lang niets binnenkomt

# Volgorde van de tekens die de computer stuurt (moet exact overeenkomen met
# de lijst 'volgorde' in stuur_robot.py)
VOORUIT = 0
LINKS = 1
ACHTERUIT = 2
RECHTS = 3
NULPUNT = 4       # R: nieuwe opname beginnen
STOPPEN = 5
LA_PLUS = 6       # linker attachment +
LA_MIN = 7        # linker attachment -
RA_PLUS = 8       # rechter attachment +
RA_MIN = 9        # rechter attachment -
PRECISIE = 10
STAPMODUS = 11
# AANGEPAST (nieuw): vier extra tekens
STAP_KLAAR = 12   # SPATIE of ENTER: de huidige stap nu afsluiten
ONGEDAAN = 13     # BACKSPACE: laatste stap wissen en terugrijden
AFSPELEN = 14     # P: alles afspelen op wedstrijdsnelheid
STAPGROOTTE = 15  # dit teken is geen 0 of 1, maar "1", "2" of "3"
AANTAL_TEKENS = 16

# AANGEPAST (nieuw): het "versienummer" van de afspraken tussen computer en
# hub. stuur_robot.py stuurt pas commando's als het dit nummer ziet. Zo kan
# een oude stuur_robot.py nooit per ongeluk een nieuwe hub besturen (of
# omgekeerd): dan zouden de toetsen door elkaar lopen.
PROTOCOL = 3


# =====================================================================
# HULPFUNCTIES
# =====================================================================

def ingedrukt(cmd, nummer):
    """Is deze toets op dit moment ingedrukt?"""
    return cmd[nummer:nummer + 1] == b"1"


def net_ingedrukt(cmd, vorige_cmd, nummer):
    """Is deze toets NET ingedrukt (nu wel, de vorige keer nog niet)?
    Zo telt een toets die je ingedrukt houdt maar als één tik."""
    return ingedrukt(cmd, nummer) and not ingedrukt(vorige_cmd, nummer)


def rij_instellingen():
    """Snelheden en gyro-regeling voor het rijden met het toetsenbord."""
    if GEBRUIK_EIGEN_PID:
        # Ingebouwde gyro-correctie UIT: onze eigen PID doet die taak.
        # Zo werken ze niet tegen elkaar in.
        DRIVE_BASE.use_gyro(False)
    else:
        DRIVE_BASE.use_gyro(True)
    DRIVE_BASE.settings(straight_speed=100, straight_acceleration=200,
                        turn_rate=30, turn_acceleration=100)


def nulpunt_zetten():
    """Afstand, richting en attachment-hoeken hier op 0 zetten."""
    DRIVE_BASE.reset()
    HUB.imu.reset_heading(0)
    LEFT_ATTACHMENT.reset_angle(0)
    RIGHT_ATTACHMENT.reset_angle(0)


def stop_alles():
    DRIVE_BASE.stop()
    LEFT_ATTACHMENT.hold()
    RIGHT_ATTACHMENT.hold()


def soort_beweging(cmd):
    """AANGEPAST (nieuw): welke SOORT beweging vraag je nu met de toetsen?
    Geeft "rijden", "draaien", "bocht", "links_att", "rechts_att" terug,
    of None als je niets indrukt. Verandert de soort, dan begint er een
    nieuwe stap in de opname."""
    rijden = ingedrukt(cmd, VOORUIT) or ingedrukt(cmd, ACHTERUIT)
    draaien = ingedrukt(cmd, LINKS) or ingedrukt(cmd, RECHTS)
    if rijden and draaien:
        return "bocht"
    if rijden:
        return "rijden"
    if draaien:
        return "draaien"
    if ingedrukt(cmd, LA_PLUS) or ingedrukt(cmd, LA_MIN):
        return "links_att"
    if ingedrukt(cmd, RA_PLUS) or ingedrukt(cmd, RA_MIN):
        return "rechts_att"
    return None


def lees_metingen():
    """Waar staat de robot nu? Een dictionary met 4 metingen."""
    return {
        "afstand": DRIVE_BASE.distance(),     # mm, gemeten met de wielen
        "hoek": HUB.imu.heading(),            # graden, gemeten met de gyro
        "links": LEFT_ATTACHMENT.angle(),     # motorgraden
        "rechts": RIGHT_ATTACHMENT.angle(),
    }


def verschil_sinds(begin):
    """Hoeveel is de robot bewogen sinds de metingen in 'begin'?
    Geeft 4 getallen terug: afstand, hoek, links, rechts."""
    nu = lees_metingen()
    return (nu["afstand"] - begin["afstand"],
            nu["hoek"] - begin["hoek"],
            nu["links"] - begin["links"],
            nu["rechts"] - begin["rechts"])


def wacht_tot_stilstand():
    """Stopt de wielen en wacht (hoogstens 1 seconde) tot de robot echt
    stilstaat. Pas dan meten we, anders mist de stap de laatste mm."""
    DRIVE_BASE.stop()
    klok = StopWatch()
    while klok.time() < 1000:
        # state() geeft 4 getallen: afstand, snelheid, hoek, draaisnelheid
        toestand = DRIVE_BASE.state()
        if abs(toestand[1]) < 5 and abs(toestand[3]) < 5:
            break
        wait(10)
    wait(50)


def maak_stappen(afstand, hoek, links, rechts):
    """Maakt van een gemeten beweging stappen voor missies.py.
    Geeft een lijst terug (leeg als de robot amper bewoog)."""
    stappen = []
    afstand = round(afstand)
    hoek = round(hoek)

    if abs(afstand) >= BOCHT_MIN_AFSTAND and abs(hoek) >= BOCHT_MIN_HOEK:
        # Gereden EN gedraaid: een bocht. Pybricks wil de straal van de
        # cirkel en hoeveel graden je over die cirkel rijdt.
        # Een booglengte is straal x hoek (de hoek in radialen: graden
        # maal pi gedeeld door 180). Dus: straal = afstand / hoek_in_radialen.
        # Zo werken de tekens (+ of -) bij Pybricks:
        #   straal positief = vooruit, straal negatief = achteruit
        #   graden positief = naar rechts als je vooruit rijdt
        # Rijd je achteruit, dan keert het teken van de graden om.
        straal = round(afstand / abs(hoek * math.pi / 180))
        if afstand > 0:
            graden = hoek
        else:
            graden = -hoek
        stappen.append(("curve", straal, graden))
    else:
        if abs(afstand) >= MIN_AFSTAND:
            stappen.append(("straight", afstand))
        if abs(hoek) >= MIN_HOEK:
            stappen.append(("turn", hoek))

    if abs(links) >= MIN_ATTACHMENT:
        stappen.append(("run_angle", LEFT_ATTACHMENT,
                        ATTACHMENT_SNELHEID_IN_MISSIE, round(links)))
    if abs(rechts) >= MIN_ATTACHMENT:
        stappen.append(("run_angle", RIGHT_ATTACHMENT,
                        ATTACHMENT_SNELHEID_IN_MISSIE, round(rechts)))
    return stappen


def stap_als_tekst(stap):
    """Schrijft een stap als tekst, precies zoals in missies.py, bv.
    ("straight", 412),   Die tekst sturen we naar de computer."""
    tekst = '("' + stap[0] + '"'
    # stap[1:] betekent: alles van de stap behalve het eerste element
    for waarde in stap[1:]:
        if waarde == LEFT_ATTACHMENT:
            tekst += ", LEFT_ATTACHMENT"
        elif waarde == RIGHT_ATTACHMENT:
            tekst += ", RIGHT_ATTACHMENT"
        else:
            tekst += ", " + str(waarde)
    return tekst + "),"


def keer_om(stap):
    """Voert een stap ACHTERSTEVOREN uit, zodat de robot terugkeert naar
    waar hij voor die stap stond (voor BACKSPACE)."""
    soort = stap[0]
    if soort == "straight":
        safe_straight(-stap[1])
        wacht_tot_stilstand()
    elif soort == "turn":
        safe_turn(-stap[1])
        wacht_tot_stilstand()
    elif soort == "curve":
        safe_curve(-stap[1], stap[2])    # dezelfde cirkel, achteruit
        wacht_tot_stilstand()
    elif soort == "run_angle":
        safe_run_angle(stap[1], stap[2], -stap[3])


# =====================================================================
# DE OPNAME
# =====================================================================
# AANGEPAST (nieuw): alles wat de opname moet onthouden, staat in deze
# variabelen buiten de functies. Daarom staat er in de functies 'global'.
opname = []              # de opgenomen stappen, bv. [("straight", 412), ...]
eerste_nummer = 0        # welk stapnummer de eerste opgenomen stap krijgt
begin_van_stap = {}      # metingen op het moment dat de huidige stap begon
# Kwam je uit de testmodus? Dan staan hier de stappen van de missie die de
# robot al gereden had, en van welke missie en welke stap ze komen.
vooraf = []
vooraf_missie = ""
vooraf_start = 0


def nieuwe_opname():
    """Wist de opname en begint opnieuw, met de robot op 0."""
    global begin_van_stap
    opname.clear()     # clear() maakt de lijst leeg
    nulpunt_zetten()
    begin_van_stap = lees_metingen()
    # De computer luistert naar regels die beginnen met NIEUW, STAP of WEG
    if vooraf:
        # bv. "NIEUW 5 B 0": nieuwe stappen vanaf nummer 5, na missie B
        # vanaf stap 0
        print("NIEUW", eerste_nummer, vooraf_missie, vooraf_start)
    else:
        print("NIEUW", eerste_nummer)


def sluit_stap():
    """Sluit de huidige stap af: meten, stappen maken, doorsturen."""
    global begin_van_stap
    wacht_tot_stilstand()
    afstand, hoek, links, rechts = verschil_sinds(begin_van_stap)
    nieuwe_stappen = maak_stappen(afstand, hoek, links, rechts)
    for stap in nieuwe_stappen:
        opname.append(stap)
        print("STAP", eerste_nummer + len(opname) - 1, stap_als_tekst(stap))
    # Was de beweging te klein voor een stap? Dan beginnen we NIET opnieuw
    # te tellen: die paar mm tellen dan mee bij de volgende stap.
    if nieuwe_stappen:
        begin_van_stap = lees_metingen()
    HUB.display.number(eerste_nummer + len(opname))


def laatste_stap_ongedaan():
    """Wist de laatste stap en rijdt de robot terug naar waar hij voor
    die stap stond. Zo kan je een foute beweging opnieuw proberen."""
    global begin_van_stap
    sluit_stap()    # eerst de beweging van nu ook als stap bewaren
    if not opname:
        print("Er is geen stap om ongedaan te maken.")
        return
    stap = opname.pop()    # pop() haalt het laatste element uit de lijst
    keer_om(stap)
    begin_van_stap = lees_metingen()
    print("WEG", eerste_nummer + len(opname))
    HUB.display.number(eerste_nummer + len(opname))


def afspelen():
    """AANGEPAST (nieuw): speelt alles af zoals in een echte missie: op
    wedstrijdsnelheid en met de gyro aan. Eerst de stappen van de missie
    die de robot al gereden had (uit de testmodus), daarna de opname.
    Zet de robot eerst met de hand terug op de startplek!"""
    global begin_van_stap
    sluit_stap()
    # lijst + lijst = de twee lijsten achter elkaar
    alle_stappen = vooraf + opname
    if not alle_stappen:
        print("Er is nog niets om af te spelen.")
        return
    print("Afspelen op wedstrijdsnelheid. Stoppen: MIDDEN op de hub.")
    HUB.light.on(Color.ORANGE)
    try:
        start_missie()       # nulpunt hier + wedstrijdsnelheid, gyro aan
        voer_stappen_uit(alle_stappen)
        HUB.speaker.beep(600, 100)
        print("Afspelen klaar. Je kan verder rijden en opnemen.")
    except MissionStop:
        DRIVE_BASE.stop()
        LEFT_ATTACHMENT.stop()
        RIGHT_ATTACHMENT.stop()
        print("Afspelen gestopt met de knop. Je kan verder rijden en opnemen.")
        wacht_tot_losgelaten()   # anders stopt ook het vrij rijden meteen
    # Terug naar de snelheden van het toetsenbord-rijden. De volgende stap
    # begint op de plek waar de robot nu staat.
    rij_instellingen()
    begin_van_stap = lees_metingen()
    HUB.light.on(Color.WHITE)
    HUB.display.number(eerste_nummer + len(opname))


# =====================================================================
# HET HOOFDPROGRAMMA
# =====================================================================

def vrij_rijden(vooraf_stappen=None, missie="", start=0):
    """Rijden met het toetsenbord en alles opnemen. Stopt met ESC op de
    computer of met de middelste knop op de hub.
    AANGEPAST: de testmodus van main.py geeft mee welke stappen van welke
    missie de robot al gereden heeft:
      vooraf_stappen: die stappen (een lijst), of None als er geen zijn
      missie: de letter van de missie, bv. "B"
      start: het nummer van de eerste van die stappen
    De nieuwe stappen krijgen dan de nummers die erna komen."""
    global vooraf, vooraf_missie, vooraf_start, eerste_nummer
    if vooraf_stappen is None:
        vooraf = []
    else:
        vooraf = vooraf_stappen
    vooraf_missie = missie
    vooraf_start = start
    eerste_nummer = start + len(vooraf)

    rij_instellingen()
    HUB.light.on(Color.WHITE)

    toetsenbord = poll()
    toetsenbord.register(stdin)

    # AANGEPAST: oude tekens die nog van een vorige keer klaarstaan, weggooien
    while toetsenbord.poll(0):
        stdin.buffer.read(1)

    # Geheugen van de PID-regeling
    doel_hoek = 0          # de richting die de robot moet aanhouden
    integraal = 0
    vorige_hoek = 0
    draaisnelheid_gefilterd = 0
    klok = StopWatch()
    vorige_tijd = klok.time()

    leeg = b"0" * AANTAL_TEKENS
    cmd = leeg
    vorige_cmd = leeg
    binnen = b""             # AANGEPAST: hier komen de tekens één voor één binnen
    stapmodus = False
    stapgrootte = "2"
    huidige_soort = None     # AANGEPAST: welke soort beweging de huidige stap is
    teller = 0

    laatste_bericht = StopWatch()
    veiligheidsstop_gedaan = False

    print("Vrij rijden gestart. Opname loopt.")
    print("PROTOCOL", PROTOCOL)
    nieuwe_opname()
    HUB.display.number(eerste_nummer)
    stdout.buffer.write(b"rdy")   # laat de computer weten: stuur maar

    try:
        while True:
            # --- VEILIGHEID 1: de knop op de hub stopt ALTIJD ---
            if Button.CENTER in HUB.buttons.pressed():
                print("Gestopt met de knop op de hub.")
                break

            # --- NIEUW COMMANDO? (zonder te wachten: de lus loopt gewoon door) ---
            # AANGEPAST: elk commando eindigt nu met een Enter-teken (\n).
            # We lezen teken per teken en wachten nooit op tekens die
            # misschien niet komen. Zo kan de hub nooit vastlopen.
            while toetsenbord.poll(0):
                teken = stdin.buffer.read(1)
                if teken == b"\n":
                    if len(binnen) == AANTAL_TEKENS:
                        cmd = binnen
                        laatste_bericht.reset()
                        veiligheidsstop_gedaan = False
                    binnen = b""
                    stdout.buffer.write(b"rdy")
                    break     # eerst dit commando verwerken
                binnen += teken

            # --- VEILIGHEID 2: te lang niets ontvangen = stoppen ---
            if laatste_bericht.time() > VEILIGHEID_TIMEOUT:
                if not veiligheidsstop_gedaan:
                    print("Geen verbinding: motoren uit veiligheid gestopt.")
                    if binnen:
                        # Er komen wel tekens binnen, maar geen geldige commando's
                        print("Past stuur_robot.py niet bij deze code? Download de nieuwste.")
                    stop_alles()
                    veiligheidsstop_gedaan = True
                vorige_cmd = leeg
                wait(LUS_TIJD)
                continue

            if ingedrukt(cmd, STOPPEN):
                break

            # Echte verstreken tijd sinds de vorige lus, nodig voor de PID
            nu = klok.time()
            dt = (nu - vorige_tijd) / 1000
            if dt <= 0:
                dt = 0.001
            vorige_tijd = nu

            hoek = HUB.imu.heading()

            # Hoe snel draait de robot nu? Uitgemiddeld, zodat ruis geen stoten geeft.
            draaisnelheid = (hoek - vorige_hoek) / dt
            draaisnelheid_gefilterd = 0.8 * draaisnelheid_gefilterd + 0.2 * draaisnelheid
            vorige_hoek = hoek

            # --- AANGEPAST (nieuw): de opname ---
            # Moet de robot een stilstaande actie doen (opname wissen, stap
            # afsluiten, ongedaan maken)? Dan is 'iets_gedaan' True en zetten
            # we daarna de PID opnieuw klaar.
            iets_gedaan = False

            if net_ingedrukt(cmd, vorige_cmd, NULPUNT):
                # R: helemaal opnieuw beginnen op de plek waar de robot nu staat
                wacht_tot_stilstand()
                nieuwe_opname()
                huidige_soort = None
                iets_gedaan = True

            if net_ingedrukt(cmd, vorige_cmd, STAP_KLAAR):
                # SPATIE of ENTER: de huidige stap nu afsluiten
                sluit_stap()
                huidige_soort = None
                print("KLAAR")      # de computer weet zo dat alles binnen is
                iets_gedaan = True

            if net_ingedrukt(cmd, vorige_cmd, ONGEDAAN):
                # BACKSPACE: laatste stap wissen en terugrijden
                laatste_stap_ongedaan()
                huidige_soort = None
                iets_gedaan = True

            if net_ingedrukt(cmd, vorige_cmd, AFSPELEN):
                # P: alles afspelen op wedstrijdsnelheid
                afspelen()
                huidige_soort = None
                iets_gedaan = True
                laatste_bericht.reset()   # het afspelen duurde lang, dat is geen verbindingsfout

            # Begin je aan een ANDERE soort beweging? Dan is de vorige stap klaar.
            soort = soort_beweging(cmd)
            if soort is not None and soort != huidige_soort:
                if huidige_soort is not None:
                    sluit_stap()
                    iets_gedaan = True
                huidige_soort = soort

            if iets_gedaan:
                # De robot stond even stil: de richting van nu is het nieuwe
                # doel, en de PID begint opnieuw (anders maakt hij een sprong).
                hoek = HUB.imu.heading()
                vorige_hoek = hoek
                doel_hoek = hoek
                integraal = 0
                draaisnelheid_gefilterd = 0
                vorige_tijd = klok.time()

            # AANGEPAST (nieuw): stapgrootte kiezen met de cijfertoetsen.
            # cmd[STAPGROOTTE] is een getal (de code van het teken), chr()
            # maakt daar weer het teken "1", "2" of "3" van.
            keuze = chr(cmd[STAPGROOTTE])
            if keuze in STAPGROOTTES and keuze != stapgrootte:
                stapgrootte = keuze
                print("Stapgrootte", keuze, ":", STAPGROOTTES[keuze])

            if net_ingedrukt(cmd, vorige_cmd, STAPMODUS):
                stapmodus = not stapmodus
                DRIVE_BASE.stop()
                if stapmodus:
                    print("Stapmodus AAN")
                else:
                    print("Stapmodus UIT")

            if stapmodus:
                # --- STAPMODUS: elke tik = één kleine, exacte beweging ---
                stap_mm, stap_graden, stap_att = STAPGROOTTES[stapgrootte]
                # AANGEPAST: de safe_-versies, zodat de knop op de hub ook
                # tijdens een stap kan stoppen
                if net_ingedrukt(cmd, vorige_cmd, VOORUIT):
                    safe_straight(stap_mm)
                elif net_ingedrukt(cmd, vorige_cmd, ACHTERUIT):
                    safe_straight(-stap_mm)
                elif net_ingedrukt(cmd, vorige_cmd, LINKS):
                    safe_turn(-stap_graden)
                elif net_ingedrukt(cmd, vorige_cmd, RECHTS):
                    safe_turn(stap_graden)

                if net_ingedrukt(cmd, vorige_cmd, LA_PLUS):
                    safe_run_angle(LEFT_ATTACHMENT, 100, stap_att)
                elif net_ingedrukt(cmd, vorige_cmd, LA_MIN):
                    safe_run_angle(LEFT_ATTACHMENT, 100, -stap_att)
                if net_ingedrukt(cmd, vorige_cmd, RA_PLUS):
                    safe_run_angle(RIGHT_ATTACHMENT, 100, stap_att)
                elif net_ingedrukt(cmd, vorige_cmd, RA_MIN):
                    safe_run_angle(RIGHT_ATTACHMENT, 100, -stap_att)

                # na een stap: de huidige richting is de nieuwe doelrichting
                doel_hoek = HUB.imu.heading()
                vorige_hoek = doel_hoek
                integraal = 0

            else:
                # --- GEWOON RIJDEN: toets ingedrukt houden ---
                if ingedrukt(cmd, PRECISIE):
                    rij = PRECIEZE_RIJSNELHEID
                    draai = PRECIEZE_DRAAISNELHEID
                    att = PRECIEZE_ATTACHMENT_SNELHEID
                else:
                    rij = RIJSNELHEID
                    draai = DRAAISNELHEID
                    att = ATTACHMENT_SNELHEID

                snelheid = 0
                draaien = 0
                if ingedrukt(cmd, VOORUIT):
                    snelheid += rij
                if ingedrukt(cmd, ACHTERUIT):
                    snelheid -= rij
                if ingedrukt(cmd, LINKS):
                    draaien -= draai
                if ingedrukt(cmd, RECHTS):
                    draaien += draai

                if not GEBRUIK_EIGEN_PID or draaien != 0 or snelheid == 0:
                    # Ingebouwde regeling, of je draait bewust, of je staat stil:
                    # de richting waar de robot NU naar kijkt wordt het nieuwe doel.
                    doel_hoek = hoek
                    integraal = 0
                    DRIVE_BASE.drive(snelheid, draaien)
                else:
                    # Rechtdoor rijden met onze eigen PID
                    fout = doel_hoek - hoek
                    if abs(fout) < DODE_ZONE:
                        fout = 0   # zo klein dat het ruis is: niet op reageren

                    integraal += fout * dt
                    if integraal > MAX_INTEGRAAL:
                        integraal = MAX_INTEGRAAL
                    if integraal < -MAX_INTEGRAAL:
                        integraal = -MAX_INTEGRAAL

                    # D-deel: remt af als de robot al aan het terugdraaien is.
                    # We gebruiken de uitgemiddelde draaisnelheid, niet het
                    # verschil tussen twee losse metingen (dat geeft stoten).
                    afgeleide = -draaisnelheid_gefilterd

                    correctie = KP * fout + KI * integraal + KD * afgeleide
                    if correctie > MAX_CORRECTIE:
                        correctie = MAX_CORRECTIE
                    if correctie < -MAX_CORRECTIE:
                        correctie = -MAX_CORRECTIE

                    DRIVE_BASE.drive(snelheid, correctie)

                # Attachments: run() houdt de snelheid constant, ook heel traag
                if ingedrukt(cmd, LA_PLUS):
                    LEFT_ATTACHMENT.run(att)
                elif ingedrukt(cmd, LA_MIN):
                    LEFT_ATTACHMENT.run(-att)
                else:
                    LEFT_ATTACHMENT.hold()

                if ingedrukt(cmd, RA_PLUS):
                    RIGHT_ATTACHMENT.run(att)
                elif ingedrukt(cmd, RA_MIN):
                    RIGHT_ATTACHMENT.run(-att)
                else:
                    RIGHT_ATTACHMENT.hold()

            vorige_cmd = cmd

            # Om de 10 lussen (= 10 keer per seconde) doorsturen hoeveel de
            # robot bewogen is in de HUIDIGE stap.
            # AANGEPAST: vroeger de totalen sinds het nulpunt, nu enkel deze stap.
            teller += 1
            if teller % 10 == 0:
                afstand, hoek_stap, links, rechts = verschil_sinds(begin_van_stap)
                print("nu afstand=%d hoek=%d links=%d rechts=%d"
                      % (afstand, hoek_stap, links, rechts))

            wait(LUS_TIJD)

    except MissionStop:
        # De middelste knop werd ingedrukt tijdens een stap (safe_...)
        print("Gestopt met de knop op de hub.")

    # De laatste beweging ook nog als stap bewaren
    stop_alles()
    sluit_stap()
    print("EINDE")
    stop_alles()


# AANGEPAST: dit stuk loopt ENKEL als je vrij_rijden.py zelf start. Haalt
# main.py dit bestand op met 'import', dan is __name__ niet "__main__" en
# start het rijden pas als je in het menu de letter V kiest.
if __name__ == "__main__":
    vrij_rijden()
    # Extra veiligheidsnet
    DRIVE_BASE.stop()
    LEFT_ATTACHMENT.stop()
    RIGHT_ATTACHMENT.stop()
