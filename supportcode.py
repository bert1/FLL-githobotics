# =====================================================================
# supportcode.py: DE GEREEDSCHAPSKIST VAN DE ROBOT
# =====================================================================
# Dit bestand voer je nooit zelf uit. De andere bestanden (main.py,
# missies.py, vrij_rijden.py) halen hier hun onderdelen uit met 'import'.
# Hier staat:
#   1. hoe de robot gebouwd is (welke motor op welke poort, wielmaat)
#   2. veilige rij-functies die stoppen als je op de middelste knop drukt
#   3. hulpjes voor het menu
#   4. snelheidsprofielen (precies of snel)
#   5. het stappen-systeem dat een missie uitvoert
#   6. een extra krachtige manier om rechtdoor te rijden
# Uitleg voor beginners: zie README.md
# =====================================================================

import math
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Direction, Port, Axis, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# --- 1. ROBOT SETUP ---
# Hier stellen we de robot één keer in voor alle programma's
HUB = PrimeHub(top_side=Axis.Z, front_side=Axis.X)

# Motoren definieren
# Aandrijving: linker wiel op poort C (tegenwijzerzin = vooruit),
#              rechter wiel op poort D (wijzerzin = vooruit)
Left_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
Right_Motor = Motor(Port.D, Direction.CLOCKWISE)
# Attachments: poort C is nu bezet door het linker wiel, daarom zit de linker
# attachment-motor op poort E. Klopt dit niet met jullie robot? Pas hier de poort aan.
LEFT_ATTACHMENT = Motor(Port.E, Direction.CLOCKWISE)
RIGHT_ATTACHMENT = Motor(Port.F, Direction.CLOCKWISE)

# DriveBase instellingen
WHEEL_DIAMETER = 62.4
AXLE_TRACK = 153

DRIVE_BASE = DriveBase(Left_motor, Right_Motor, WHEEL_DIAMETER, AXLE_TRACK)

# Standaard snelheden (precieze modus, zoals in je originele code)
DEFAULT_SPEED = 700
DEFAULT_ACCEL = 400
DEFAULT_TURN_SPEED = 500
DEFAULT_TURN_ACCEL = 250

# Snelheden voor de "sprint" op het einde van een missie, als je gewoon zo
# snel mogelijk terug naar de basis rijdt en precisie niet meer telt.
RETURN_SPEED = 1000
RETURN_ACCEL = 1000

DRIVE_BASE.settings(straight_speed=DEFAULT_SPEED,
                    straight_acceleration=DEFAULT_ACCEL,
                    turn_rate=DEFAULT_TURN_SPEED,
                    turn_acceleration=DEFAULT_TURN_ACCEL)

# --- 2. VEILIGHEIDS FUNCTIES (SAFE WRAPPERS) ---
# Deze functies zijn ongewijzigd t.o.v. vorig seizoen: ze werken betrouwbaar,
# dus we raken er niets aan.
class MissionStop(Exception):
    """Speciale foutmelding om een missie te onderbreken"""
    pass

def check_stop():
    """Check constant of de Center-knop is ingedrukt. Zo ja: STOP ALLES."""
    if Button.CENTER in HUB.buttons.pressed():
        DRIVE_BASE.stop()
        LEFT_ATTACHMENT.stop()
        RIGHT_ATTACHMENT.stop()
        HUB.light.on(Color.RED)
        HUB.speaker.beep(100, 500)
        raise MissionStop("Stop knop ingedrukt!")

def safe_straight(distance):
    """Rijdt rechtdoor, maar stopt als je op de knop drukt."""
    DRIVE_BASE.straight(distance, wait=False)
    while not DRIVE_BASE.done():
        check_stop()
        wait(10)

def safe_turn(angle):
    """Draait, maar stopt als je op de knop drukt."""
    DRIVE_BASE.turn(angle, wait=False)
    while not DRIVE_BASE.done():
        check_stop()
        wait(10)

def safe_curve(radius, angle):
    """Rijdt in een bocht, maar stopt als je op de knop drukt."""
    DRIVE_BASE.curve(radius, angle, wait=False)
    while not DRIVE_BASE.done():
        check_stop()
        wait(10)

def safe_wait(time_ms):
    """Wacht een bepaalde tijd, maar stopt als je op de knop drukt."""
    timer = StopWatch()
    while timer.time() < time_ms:
        check_stop()
        wait(10)

def safe_run_angle(motor, speed, angle, then=Stop.HOLD):
    """Draait een attachment motor, maar stopt als je op de knop drukt.

    then: wat de motor doet als hij klaar is.
          Stop.HOLD  = vastklemmen op die hoek (standaard)
          Stop.COAST = loslaten, de motor mag vrij uitdraaien
          Stop.BRAKE = afremmen, maar niet vastklemmen
    """
    # AANGEPAST: vroeger werd 'then' wel meegegeven aan deze functie, maar
    # nooit doorgegeven aan run_angle(). Daardoor deed een stap zoals
    # ("run_angle", LEFT_ATTACHMENT, 200, 90, Stop.COAST) toch altijd HOLD.
    # Nu geven we 'then' wel door, zodat de motor doet wat je vraagt.
    motor.run_angle(speed, angle, then=then, wait=False)
    while not motor.done():
        check_stop()
        wait(10)

# --- 3. MENU NAVIGATIE ---
def prior_program(active, prog_list):
    """Gaat eentje terug in de lijst (en draait rond als je bij het begin bent)"""
    active = (active - 1) % len(prog_list)
    return active

def next_program(active, prog_list):
    """Gaat eentje verder in de lijst (en draait rond als je bij het einde bent)"""
    active = (active + 1) % len(prog_list)
    return active

# --- 4. SNELHEIDSPROFIELEN ---
# In plaats van in elke missie opnieuw DRIVE_BASE.settings(...) met dezelfde
# getallen te herhalen: gebruik deze twee functies.
def set_precieze_modus():
    """Voorzichtige, nauwkeurige snelheid met gyro-correctie aan.
    Dit is de normale modus tijdens een missie."""
    DRIVE_BASE.use_gyro(True)
    DRIVE_BASE.settings(straight_speed=DEFAULT_SPEED,
                        straight_acceleration=DEFAULT_ACCEL,
                        turn_rate=DEFAULT_TURN_SPEED,
                        turn_acceleration=DEFAULT_TURN_ACCEL)

def set_snelle_modus():
    """Hoge snelheid, gyro uit. Gebruik dit enkel op het einde van een missie,
    als je gewoon zo snel mogelijk terug naar de basis rijdt en de precieze
    positie niet meer belangrijk is."""
    DRIVE_BASE.use_gyro(False)
    DRIVE_BASE.settings(straight_speed=RETURN_SPEED,
                        straight_acceleration=RETURN_ACCEL)

def stop_attachments():
    """Stopt beide attachment-motoren (laat ze los i.p.v. vast te blijven houden).
    Roep dit aan het einde van elke missie aan."""
    LEFT_ATTACHMENT.stop()
    RIGHT_ATTACHMENT.stop()

def start_missie():
    """Roep dit aan bij de start van ELKE missie, vlak voor de eerste beweging.

    Dit 'nult' de positie en de richting van de robot op de plek waar hij nu
    op de mat staat neergezet. Zonder dit blijft DRIVE_BASE de hoek van de
    vorige missie onthouden: als je de robot met de hand op een iets andere
    hoek neerzet dan waar de vorige missie eindigde, tellen die kleine
    verschillen op tot echte afwijkingen tijdens de missie. Dit is de
    belangrijkste verandering voor de PRECISIE van de missies."""
    HUB.imu.reset_heading(0)
    DRIVE_BASE.reset()
    set_precieze_modus()

# --- 5. STAPPEN-SYSTEEM VOOR MISSIES ---
# Een missie schrijven we niet meer als een lange rits losse aanroepen, maar
# als een LIJST van stappen. Elke stap is een tuple: het eerste element zegt
# WELKE actie het is, de rest zijn de argumenten voor die actie. Zie missies.py
# voor voorbeelden.
#
# Het grote voordeel: je kan met start_bij= een missie op eender welke stap
# laten BEGINNEN. Zo test je één stuk van een missie apart, zonder de hele
# missie van bij het begin te moeten herhalen.
def voer_stappen_uit(stappen, start_bij=0, eind_stap=None):
    """Voert een lijst van stappen uit.
    stappen: lijst van tuples, bv. ("straight", 590) of ("turn", 62)
    start_bij: indexnummer van de stap waarmee je wil beginnen (0 = eerste stap)
    eind_stap: indexnummer waarna gestopt wordt (niet inbegrepen). Standaard None
               = tot het einde van de missie. Gebruik dit om maar EEN klein
               stukje van een missie te testen, zonder de rest te moeten
               afwachten (zie test_modus() in main.py).
    """
    if eind_stap is None:
        eind_stap = len(stappen)

    for i, stap in enumerate(stappen):
        if i < start_bij:
            continue  # deze stap overslaan: we testen vanaf een latere stap
        if i >= eind_stap:
            break  # we hebben genoeg getest, de rest van de missie niet uitvoeren

        HUB.display.number(i)  # toon het stapnummer, handig om te volgen bij het testen
        soort = stap[0]

        if soort == "straight":
            safe_straight(stap[1])
        elif soort == "turn":
            safe_turn(stap[1])
        elif soort == "curve":
            safe_curve(stap[1], stap[2])
        elif soort == "wait":
            safe_wait(stap[1])
        elif soort == "run_angle":
            motor, snelheid, hoek = stap[1], stap[2], stap[3]
            then = stap[4] if len(stap) > 4 else Stop.HOLD
            safe_run_angle(motor, snelheid, hoek, then)
        elif soort == "snel":
            set_snelle_modus()
        elif soort == "precies":
            set_precieze_modus()
        elif soort == "gyro_uit":
            DRIVE_BASE.use_gyro(False)
        elif soort == "call":
            stap[1]()  # roept een functie zonder argumenten op, bv. een instelling
        elif soort == "herhaal":
            aantal, substappen = stap[1], stap[2]
            for _ in range(aantal):
                voer_stappen_uit(substappen, start_bij=0)
        else:
            print("Onbekende stapsoort:", soort)

# --- 6. PID GYRO-RIJDEN (VOOR SPECIALE, SNELLE RECHTE STUKKEN) ---
# BELANGRIJK om te begrijpen: DRIVE_BASE.use_gyro(True) zorgt AL voor
# gyro-gecorrigeerd rechtdoor rijden in safe_straight(). Voor gewone
# missiestappen gebruik je dus gewoon safe_straight() zoals altijd: die is
# even nauwkeurig en veel eenvoudiger, en lost hetzelfde probleem op.
#
# safe_gyro_sprint() hieronder is GEEN vervanging daarvan. Ze bestaat voor één
# specifiek geval: wanneer je de motoren op volle, RUWE kracht (dc = direct
# duty cycle, zonder de rustige optrek/afrem-curve die DRIVE_BASE gebruikt)
# recht vooruit wil duwen, bijvoorbeeld om iets met kracht te forceren of om
# zo snel mogelijk te vertrekken. Gebruik ze dus enkel als je in de praktijk
# merkt dat safe_straight() daar niet snel/krachtig genoeg voor is.
def safe_gyro_sprint(speed, afstand_mm, doel_hoek=None):
    """Rijdt rechtdoor op volle motorkracht, met eigen gyro-correctie.

    speed: motorkracht (dc-percentage, ongeveer -100 tot 100). Negatief = achteruit.
    afstand_mm: hoever de robot moet rijden, in millimeter (net zoals bij safe_straight)
    doel_hoek: de richting die de robot moet aanhouden in graden; standaard de
               richting waarin de robot NU al staat (dus gewoon rechtdoor)
    """
    kp = 4
    kd = 10
    ki = 0.05

    if doel_hoek is None:
        doel_hoek = HUB.imu.heading()

    # De motoren tellen in graden, niet in millimeter. Omtrek van het wiel
    # = pi * diameter. Daarmee zetten we millimeter om naar motorgraden.
    omtrek = math.pi * WHEEL_DIAMETER
    graden_nodig = abs((afstand_mm / omtrek) * 360)

    Left_motor.reset_angle(0)
    Right_Motor.reset_angle(0)

    last_error = 0
    integral = 0
    timer = StopWatch()
    last_time = timer.time()

    while True:
        check_stop()  # zo kan de middelste knop dit ook onderbreken

        gemiddelde_hoek = (abs(Left_motor.angle()) + abs(Right_Motor.angle())) / 2
        if gemiddelde_hoek >= graden_nodig:
            break

        # Echte verstreken tijd sinds de vorige lus (in seconden), in plaats
        # van te rekenen alsof elke lus precies 10 ms duurt. Zo blijft de
        # regeling correct, ook als de lus eens iets trager loopt.
        nu = timer.time()
        dt = (nu - last_time) / 1000
        if dt <= 0:
            dt = 0.001
        last_time = nu

        error = doel_hoek - HUB.imu.heading()
        afgeleide = (error - last_error) / dt
        integral += error * dt
        correctie = (kp * error) + (kd * afgeleide) + (ki * integral)

        Right_Motor.dc(speed - correctie)
        Left_motor.dc(speed + correctie)
        last_error = error
        wait(10)

    Left_motor.dc(0)
    Right_Motor.dc(0)
