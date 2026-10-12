# =====================================================================
# missies.py: HIER SCHRIJVEN JULLIE DE MISSIES
# =====================================================================
# Dit is het bestand waar jullie het meest in zullen werken.
#
# !!! NIEUW SEIZOEN: BIOGLOW FOUNDERS EDITION !!!
# De missies van vorig seizoen zijn verwijderd: ze passen niet bij de
# nieuwe mat. Alle missies hieronder zijn LEEG en moeten nog geschreven
# worden. Zoek naar "NIEUWE STAPPEN HIER" om te zien waar dat moet.
# (De oude missies staan nog in de geschiedenis op GitHub, als je wil
# kijken hoe ze toen gemaakt zijn.)
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
# FOUT GETYPT? Bij het opstarten kijkt main.py alle missies na. Vindt het een
#      fout, dan wordt het lampje ROOD, toont het scherm de letter en het
#      stapnummer (bv. "B 4") en staat de uitleg onderaan in Pybricks Code.
#
# TIP: met vrij_rijden.py + stuur_robot.py kan je de robot met het toetsenbord
#      naar de juiste plek rijden en met SPATIE een kant-en-klare regel krijgen
#      om hier te plakken.
#
# TIP: een getal dat je vaak bijstelt op de mat, geef je een naam bovenaan
#      de missie (bv. A_AFSTAND_NAAR_BOOM = 250). Zo pas je het op EEN
#      plaats aan. Schrijf in commentaar wat de oude waarde was.
#
# Uitleg voor beginners: zie README.md
# =====================================================================

from supportcode import LEFT_ATTACHMENT, RIGHT_ATTACHMENT, stop_attachments
from pybricks.parameters import Stop


# =====================================================================
# MISSIE A: (schrijf hier welke missie op de mat dit is)
# =====================================================================
# Getallen die je vaak bijstelt, zet je hier met een naam. Bijvoorbeeld:
#   A_AFSTAND_NAAR_BOOM = 250     # was 240

MISSIE_A = [
    # ---- NIEUWE STAPPEN HIER ----
    # Zo ziet een missie eruit (haal het # weg om een regel te gebruiken):
    #   ("straight", 300),                          # 30 cm vooruit
    #   ("turn", 90),                               # kwartdraai naar rechts
    #   ("run_angle", LEFT_ATTACHMENT, 200, 90),    # linker arm draaien
    #   ("snel",),                                  # snel terug naar de basis
    #   ("straight", -300),
    ("call", stop_attachments),   # laat deze regel altijd als LAATSTE staan
]


# =====================================================================
# MISSIE B: (schrijf hier welke missie op de mat dit is)
# =====================================================================
MISSIE_B = [
    # ---- NIEUWE STAPPEN HIER ----
    ("call", stop_attachments),   # laat deze regel altijd als LAATSTE staan
]


# =====================================================================
# MISSIE C: (schrijf hier welke missie op de mat dit is)
# =====================================================================
MISSIE_C = [
    # ---- NIEUWE STAPPEN HIER ----
    ("call", stop_attachments),   # laat deze regel altijd als LAATSTE staan
]


# =====================================================================
# MISSIE D: (schrijf hier welke missie op de mat dit is)
# =====================================================================
MISSIE_D = [
    # ---- NIEUWE STAPPEN HIER ----
    ("call", stop_attachments),   # laat deze regel altijd als LAATSTE staan
]


# =====================================================================
# MISSIE E: (schrijf hier welke missie op de mat dit is)
# =====================================================================
MISSIE_E = [
    # ---- NIEUWE STAPPEN HIER ----
    ("call", stop_attachments),   # laat deze regel altijd als LAATSTE staan
]


# =====================================================================
# EEN EXTRA MISSIE TOEVOEGEN (bv. F)? Doe dan deze 2 dingen:
#   1. Kopieer hierboven een volledig blok (van ===== tot ]) en noem het MISSIE_F
#   2. Voeg hieronder in MISSIE_STAPPEN de regel  "F": MISSIE_F,  toe
# Het menu in main.py neemt de nieuwe letter vanzelf over.
# =====================================================================

# Hier koppelen we elke letter van het menu aan een missie.
# main.py zoekt hierin op welke stappen bij letter A, B, ... horen.
MISSIE_STAPPEN = {
    "A": MISSIE_A,
    "B": MISSIE_B,
    "C": MISSIE_C,
    "D": MISSIE_D,
    "E": MISSIE_E,
}
