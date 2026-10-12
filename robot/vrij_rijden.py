# =====================================================================
# vrij_rijden.py: DE ROBOT BESTUREN MET HET TOETSENBORD (dit draait op de hub)
# =====================================================================
# Dit programma luistert naar commando's die stuur_robot.py vanaf de
# computer stuurt, en laat de robot rijden zolang je een toets indrukt.
# Handig om uit te zoeken hoeveel mm of graden een missie moet rijden.
# Uitleg voor beginners: zie docs/4-uitleg-code.md op GitHub
# =====================================================================

from supportcode import DRIVE_BASE, HUB, LEFT_ATTACHMENT, RIGHT_ATTACHMENT
from pybricks.parameters import Button
from pybricks.tools import wait, StopWatch

# Standaard MicroPython-modules voor het lezen van inkomende data
from usys import stdin, stdout
from uselect import poll

# --- DIT IS EEN APART TEST-PROGRAMMA, GEEN ONDERDEEL VAN main.py ---
# Laad dit programma via Pybricks Code op de hub om precies rond te rijden met
# je toetsenbord (via stuur_robot.py op je computer). Vergeet niet om na het
# tunen main.py terug op de hub te zetten voor de wedstrijd!

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
STAP_MM = 5                         # Z/S: zoveel mm per tik
STAP_GRADEN = 1                     # Q/D: zoveel graden per tik
STAP_ATTACHMENT = 5                 # I/K, O/L: zoveel motorgraden per tik

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
NULPUNT = 4
STOPPEN = 5
LA_PLUS = 6       # linker attachment +
LA_MIN = 7        # linker attachment -
RA_PLUS = 8       # rechter attachment +
RA_MIN = 9        # rechter attachment -
PRECISIE = 10
STAPMODUS = 11
AANTAL_TEKENS = 12


def ingedrukt(cmd, nummer):
    """Is deze toets op dit moment ingedrukt?"""
    return cmd[nummer:nummer + 1] == b"1"


def net_ingedrukt(cmd, vorige_cmd, nummer):
    """Is deze toets NET ingedrukt (nu wel, de vorige keer nog niet)?
    Zo telt een toets die je ingedrukt houdt maar als één tik."""
    return ingedrukt(cmd, nummer) and not ingedrukt(vorige_cmd, nummer)


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


def vrij_rijden():
    if GEBRUIK_EIGEN_PID:
        # Ingebouwde gyro-correctie UIT: onze eigen PID doet die taak.
        # Zo werken ze niet tegen elkaar in.
        DRIVE_BASE.use_gyro(False)
    else:
        DRIVE_BASE.use_gyro(True)
    DRIVE_BASE.settings(straight_speed=100, straight_acceleration=200,
                        turn_rate=30, turn_acceleration=100)
    nulpunt_zetten()

    toetsenbord = poll()
    toetsenbord.register(stdin)

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
    stapmodus = False
    teller = 0

    laatste_bericht = StopWatch()
    veiligheidsstop_gedaan = False

    print("Klaar om te rijden. Start nu stuur_robot.py op je computer.")
    stdout.buffer.write(b"rdy")   # laat de computer weten: stuur maar

    while True:
        # --- VEILIGHEID 1: de knop op de hub stopt ALTIJD ---
        if Button.CENTER in HUB.buttons.pressed():
            print("Gestopt met de knop op de hub.")
            stop_alles()
            return

        # --- NIEUW COMMANDO? (zonder te wachten: de lus loopt gewoon door) ---
        if toetsenbord.poll(0):
            cmd = stdin.buffer.read(AANTAL_TEKENS)
            stdout.buffer.write(b"rdy")
            laatste_bericht.reset()
            veiligheidsstop_gedaan = False

        # --- VEILIGHEID 2: te lang niets ontvangen = stoppen ---
        if laatste_bericht.time() > VEILIGHEID_TIMEOUT:
            if not veiligheidsstop_gedaan:
                print("Geen verbinding: motoren uit veiligheid gestopt.")
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

        if net_ingedrukt(cmd, vorige_cmd, NULPUNT):
            DRIVE_BASE.stop()
            nulpunt_zetten()
            hoek = 0
            vorige_hoek = 0
            doel_hoek = 0
            integraal = 0
            print("Nulpunt gezet.")

        if net_ingedrukt(cmd, vorige_cmd, STAPMODUS):
            stapmodus = not stapmodus
            DRIVE_BASE.stop()
            if stapmodus:
                print("Stapmodus AAN")
            else:
                print("Stapmodus UIT")

        if stapmodus:
            # --- STAPMODUS: elke tik = één kleine, exacte beweging ---
            if net_ingedrukt(cmd, vorige_cmd, VOORUIT):
                DRIVE_BASE.straight(STAP_MM)
            elif net_ingedrukt(cmd, vorige_cmd, ACHTERUIT):
                DRIVE_BASE.straight(-STAP_MM)
            elif net_ingedrukt(cmd, vorige_cmd, LINKS):
                DRIVE_BASE.turn(-STAP_GRADEN)
            elif net_ingedrukt(cmd, vorige_cmd, RECHTS):
                DRIVE_BASE.turn(STAP_GRADEN)

            if net_ingedrukt(cmd, vorige_cmd, LA_PLUS):
                LEFT_ATTACHMENT.run_angle(100, STAP_ATTACHMENT)
            elif net_ingedrukt(cmd, vorige_cmd, LA_MIN):
                LEFT_ATTACHMENT.run_angle(100, -STAP_ATTACHMENT)
            if net_ingedrukt(cmd, vorige_cmd, RA_PLUS):
                RIGHT_ATTACHMENT.run_angle(100, STAP_ATTACHMENT)
            elif net_ingedrukt(cmd, vorige_cmd, RA_MIN):
                RIGHT_ATTACHMENT.run_angle(100, -STAP_ATTACHMENT)

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

        # Om de 10 lussen (= 10 keer per seconde) de waarden doorsturen
        teller += 1
        if teller % 10 == 0:
            afstand = round(DRIVE_BASE.distance())
            hoek_rond = round(HUB.imu.heading())   # gyro: zelfde meting als in de missies
            links = round(LEFT_ATTACHMENT.angle())
            rechts = round(RIGHT_ATTACHMENT.angle())
            HUB.display.number(afstand)
            print("afstand=%d hoek=%d links=%d rechts=%d" % (afstand, hoek_rond, links, rechts))

        wait(LUS_TIJD)

    stop_alles()
    print("Gestopt.")


vrij_rijden()
# Extra veiligheidsnet
DRIVE_BASE.stop()
LEFT_ATTACHMENT.stop()
RIGHT_ATTACHMENT.stop()
