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
# Uitleg voor beginners: zie README.md
# =====================================================================

from supportcode import LEFT_ATTACHMENT, RIGHT_ATTACHMENT, stop_attachments
from pybricks.parameters import Stop

# ---------------------------------------------------------------------
# DE MISSIES HIERONDER ZIJN VOORBEELDEN.
# Vervang de getallen door wat jullie robot echt moet doen op de mat.
# ---------------------------------------------------------------------

MISSIE_A = [
    ("straight", 300),                          # stap 0: 30 cm vooruit
    ("turn", 90),                               # stap 1: kwartdraai naar rechts
    ("straight", 150),                          # stap 2: 15 cm vooruit
    ("run_angle", LEFT_ATTACHMENT, 200, 90),    # stap 3: linker arm omhoog
    ("wait", 300),                              # stap 4: even wachten
    ("run_angle", LEFT_ATTACHMENT, 200, -90),   # stap 5: linker arm terug
    ("snel",),                                  # stap 6: snel terug naar de basis
    ("straight", -150),                         # stap 7
    ("turn", -90),                              # stap 8
    ("straight", -300),                         # stap 9
]

MISSIE_B = [
    ("straight", 200),
    ("curve", 250, 45),                         # bocht naar rechts
    ("run_angle", RIGHT_ATTACHMENT, 300, 180),
    ("straight", -200),
]

MISSIE_C = [
    ("straight", 100),
    ("herhaal", 3, [                            # 3 keer duwen
        ("straight", 50),
        ("straight", -50),
    ]),
    ("straight", -100),
]

MISSIE_D = [
    ("straight", 100),
    ("straight", -100),
]

MISSIE_E = [
    ("straight", 100),
    ("straight", -100),
]

# ---------------------------------------------------------------------
# Hier koppelen we elke letter van het menu aan een missie.
# main.py zoekt hierin op welke stappen bij letter A, B, ... horen.
# Voeg je een letter toe? Voeg ze dan OOK toe aan PROGRAM_LIST in main.py.
# ---------------------------------------------------------------------
MISSIE_STAPPEN = {
    "A": MISSIE_A,
    "B": MISSIE_B,
    "C": MISSIE_C,
    "D": MISSIE_D,
    "E": MISSIE_E,
}
