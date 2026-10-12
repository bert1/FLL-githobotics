# =====================================================================
# missies.py: HIER SCHRIJVEN JULLIE DE MISSIES
# =====================================================================
# Dit is het bestand waar jullie het meest in zullen werken.
#
# Een missie is een LIJST van STAPPEN. Elke stap staat tussen haakjes ( )
# en eindigt met een komma. Het eerste woord zegt WAT de robot moet doen,
# de getallen erna zeggen HOEVEEL.
#
#   ("straight", 300)              rij 300 mm vooruit (negatief = achteruit)
#   ("turn", 90)                   draai 90 graden naar rechts (negatief = links)
#   ("curve", 200, 90)             rij een bocht met straal 200 mm over 90 graden
#   ("wait", 500)                  wacht 500 milliseconden (= een halve seconde)
#   ("run_angle", LEFT_ATTACHMENT, 200, 90)
#                                  draai de linker attachment 90 graden
#                                  aan snelheid 200 graden per seconde
#   ("run_angle", RIGHT_ATTACHMENT, 200, -90, Stop.COAST)
#                                  idem rechts, en laat de motor daarna los
#   ("snel",)                      vanaf nu snel rijden (gyro uit)
#   ("precies",)                   vanaf nu weer precies rijden (gyro aan)
#   ("gyro_uit",)                  gyro-correctie uitzetten
#   ("herhaal", 3, [ ...stappen... ])
#                                  voer de stappen tussen [ ] 3 keer uit
#
# LET OP: een stap met maar één woord heeft toch een komma nodig:
#   ("snel",)   is goed
#   ("snel")    is FOUT (dan is het geen tuple maar gewoon tekst)
#
# TIP: tel de stappen vanaf 0. De eerste stap is stap 0, de tweede stap 1, ...
#      Dat nummer zie je op het scherm van de hub tijdens het rijden, en dat
#      nummer kies je ook in de testmodus.
#
# TIP: met vrij_rijden.py + stuur_robot.py kan je de robot met het toetsenbord
#      naar de juiste plek rijden en met SPATIE een kant-en-klare regel krijgen
#      om hier te plakken.
#
# TIP: een getal dat je vaak bijstelt op de mat, geef je een naam bovenaan
#      de missie (bv. A_AFSTAND_NAAR_HAAI_1 = 66). Zo pas je het op EEN
#      plaats aan. Schrijf in commentaar wat de oude waarde was.
#
# Uitleg voor beginners: zie README.md
# =====================================================================

from supportcode import LEFT_ATTACHMENT, RIGHT_ATTACHMENT, stop_attachments
from pybricks.parameters import Stop

# =====================================================================
# MISSIE A: 1_1
# =====================================================================
# Benoemde constanten voor de waarden die dit seizoen al eens bijgesteld
# zijn. Sta je op de mat te tunen? Pas het getal hier aan, op ÉÉN plaats,
# in plaats van ergens middenin de lange lijst hieronder te zoeken.
A_AFSTAND_NAAR_HAAI_1 = 66      # was 75
A_HOEK_INSTEKEN_HAAI = 8        # was 13
A_HOEK_HAAI_GRIJPEN = 150       # was 800/100 (oude motorinstelling)
A_AFSTAND_ACHTERUIT_NA_HAAI = -255   # was -250
A_HOEK_NAAR_BORSTEL = 176       # was 172
A_HOEK_NAAR_PLANT = 50          # was 46
A_HOEK_PLANT_OPPAKKEN = -113    # was 118

MISSIE_A = [
    ("straight", 590),
    ("straight", -195),
    ("run_angle", LEFT_ATTACHMENT, 500, 90),
    ("straight", 350),
    ("turn", 62),
    ("straight", 225),
    ("run_angle", RIGHT_ATTACHMENT, 100, 90),
    ("wait", 500),
    ("straight", -100),
    ("run_angle", RIGHT_ATTACHMENT, 500, -102),
    # rijden naar haai
    ("straight", 45),
    ("turn", 35),
    ("straight", A_AFSTAND_NAAR_HAAI_1),
    ("turn", 15),
    ("straight", 105),                 # insteken haai
    ("turn", A_HOEK_INSTEKEN_HAAI),
    ("straight", 66),
    ("run_angle", RIGHT_ATTACHMENT, 999, A_HOEK_HAAI_GRIJPEN),
    ("wait", 700),
    ("straight", -50),
    ("turn", -35),
    ("straight", A_AFSTAND_ACHTERUIT_NA_HAAI),
    ("turn", A_HOEK_NAAR_BORSTEL),
    ("straight", -65),                 # borstel pakken
    ("run_angle", LEFT_ATTACHMENT, 100, -90),
    ("straight", 75),
    ("run_angle", LEFT_ATTACHMENT, 200, 75),
    ("straight", -30),
    ("turn", A_HOEK_NAAR_PLANT),       # draaien naar plant
    ("straight", -50),
    ("wait", 10),
    ("run_angle", RIGHT_ATTACHMENT, 500, A_HOEK_PLANT_OPPAKKEN),
    ("wait", 10),
    ("turn", 6),
    ("straight", 80),
    ("run_angle", RIGHT_ATTACHMENT, 500, 70),
    ("straight", -50),
    ("turn", 50),
    ("snel",),
    ("straight", -800),
    ("call", stop_attachments),
]
# Let op: de twee opeenvolgende safe_straight(0)-stappen uit de originele
# code zijn hier weggelaten. Die reden geen enkele beweging uit (0 mm) en
# kostten enkel tijd/complexiteit; kijk in je originele backup na of ze
# ooit een reden hadden (bv. wachten op DRIVE_BASE.done()) voor je verder tunet.


# =====================================================================
# MISSIE B: 12
# =====================================================================
B_AFSTAND_STUK1 = 350   # was 365
B_AFSTAND_STUK2 = 40    # was 55

MISSIE_B = [
    ("straight", 100),
    ("turn", 90),
    ("straight", 390),
    ("run_angle", LEFT_ATTACHMENT, 100, 60),
    ("wait", 200),
    ("run_angle", LEFT_ATTACHMENT, 600, -60),
    ("straight", -100),
    ("turn", -45),
    ("straight", B_AFSTAND_STUK1),
    ("turn", 45),
    ("straight", 380),
    ("turn", 86),
    ("straight", B_AFSTAND_STUK2),
    ("turn", -4),
    ("straight", 5),
    ("run_angle", RIGHT_ATTACHMENT, 300, 300),   # tandwielen
    ("straight", -6),
    ("run_angle", RIGHT_ATTACHMENT, 300, 300),
    ("turn", 15),
    ("straight", -65),
    ("snel",),
    ("turn", -65),
    ("straight", 700),
    ("call", stop_attachments),
]


# =====================================================================
# MISSIE C: 10
# =====================================================================
MISSIE_C = [
    ("straight", 230),
    ("turn", -90),
    ("straight", 480),
    ("turn", 85),
    ("straight", 55),
    ("straight", -60),
    ("run_angle", LEFT_ATTACHMENT, 400, -125),
    ("straight", -70),
    ("turn", 100),
    ("snel",),
    ("straight", 400),
    ("call", stop_attachments),
]


# =====================================================================
# MISSIE D: 5
# =====================================================================
D_HOEK_NAAR_TAFEL = -20   # was -15
D_HOEK_TERUG_VAN_TAFEL = 20   # was 15

def verhoog_grijper_versnelling():
    """Verhoogt de maximale versnelling van RIGHT_ATTACHMENT, zodat het
    schud-mechanisme in deze missie sneller heen en weer kan bewegen."""
    RIGHT_ATTACHMENT.control.limits(acceleration=6000)

MISSIE_D = [
    ("straight", 25),
    ("curve", 400, -35),
    ("straight", 60),
    ("turn", -17),
    ("turn", 55),
    ("straight", 350),
    ("turn", D_HOEK_NAAR_TAFEL),       # tafel
    ("turn", D_HOEK_TERUG_VAN_TAFEL),
    ("straight", -60),
    ("turn", 20),
    ("wait", 200),
    ("straight", -50),
    ("turn", 10),
    ("run_angle", LEFT_ATTACHMENT, 200, 90),
    ("turn", -15),
    ("wait", 10),
    ("run_angle", LEFT_ATTACHMENT, 900, -110),
    ("straight", -100),
    ("turn", -45),
    ("straight", -250),
    ("turn", 45),
    ("straight", 50),
    ("turn", -25),
    ("straight", 65),
    ("call", verhoog_grijper_versnelling),
    # LET OP, OPNIEUW TESTEN: Stop.COAST hieronder werkte vroeger NIET,
    # door een fout in safe_run_angle (supportcode.py). De motor deed toen
    # altijd HOLD (vastklemmen). Die fout is hersteld: nu laat de motor na
    # de eerste beweging echt los. Het schudden kan dus anders aanvoelen.
    # Werkt het slechter? Haal dan ", Stop.COAST" weg, dan krijg je
    # opnieuw het oude gedrag.
    ("herhaal", 6, [
        ("run_angle", RIGHT_ATTACHMENT, 700, -100, Stop.COAST),  # Stop.COAST: remt niet abrupt af
        ("run_angle", RIGHT_ATTACHMENT, 1500, 100),
    ]),
    ("turn", -15),
    ("snel",),
    ("straight", -500),
    ("call", stop_attachments),
]


# =====================================================================
# MISSIE E
# =====================================================================
E_HOEK_ARM_OMLAAG = -25   # was -45
E_HOEK_ARM_OMHOOG = 30    # was 50

MISSIE_E = [
    ("run_angle", LEFT_ATTACHMENT, 200, E_HOEK_ARM_OMLAAG),
    ("straight", 100),
    ("curve", 400, -44),
    ("straight", 20),
    ("run_angle", LEFT_ATTACHMENT, 200, E_HOEK_ARM_OMHOOG),
    ("straight", 15),
    ("straight", -100),
    ("straight", 30),
    ("run_angle", LEFT_ATTACHMENT, 200, -20),
    ("wait", 200),
    ("straight", -120),
    ("gyro_uit",),
    ("call", stop_attachments),
]

MISSIE_STAPPEN = {
    "A": MISSIE_A,
    "B": MISSIE_B,
    "C": MISSIE_C,
    "D": MISSIE_D,
    "E": MISSIE_E,
}
