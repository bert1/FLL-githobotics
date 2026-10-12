# FLL-githobotics

Github repository voor onze githobotics code in Pybricks, voor de FIRST LEGO League seizoen **BIOGLOW Founders Edition**.

Deze uitleg is geschreven voor leerlingen die nog nooit Python geprogrammeerd hebben. Lees eerst [Deel 1](#deel-1-hoe-zit-alles-in-elkaar) om te zien hoe alles samenhangt. Ken je nog geen Python? Lees dan zeker ook [Deel 3: Python basis](#deel-3-python-basis).

## Inhoud

- [Deel 1: Hoe zit alles in elkaar?](#deel-1-hoe-zit-alles-in-elkaar)
- [Deel 2: Uitleg per bestand](#deel-2-uitleg-per-bestand)
  - [supportcode.py](#supportcodepy-de-gereedschapskist)
  - [missies.py](#missiespy-hier-schrijf-jij-de-missies)
  - [main.py](#mainpy-het-wedstrijdprogramma)
  - [vrij_rijden.py en stuur_robot.py](#vrij_rijdenpy-en-stuur_robotpy-rijden-met-het-toetsenbord)
- [Deel 3: Python basis](#deel-3-python-basis)
- [Deel 4: Wat is PID?](#deel-4-wat-is-pid)
- [Woordenlijst](#woordenlijst)
- [Afspraken als je code aanpast](#afspraken-als-je-code-aanpast)

---

## Deel 1: Hoe zit alles in elkaar?

Er zijn vijf bestanden. Vier ervan draaien op de **hub** (de "hersenen" van de LEGO robot), één draait op de **computer**.

| Bestand | Waar draait het? | Wat doet het? | Moet jij hierin werken? |
|---|---|---|---|
| `missies.py` | hub | De lijst van stappen per missie | **Ja, vooral hier!** |
| `main.py` | hub | Het menu om missies te kiezen en te testen | Soms |
| `supportcode.py` | hub | Instellingen van de robot en alle hulpfuncties | Zelden |
| `vrij_rijden.py` | hub | Robot laten rijden met het toetsenbord | Enkel om in te stellen |
| `stuur_robot.py` | computer | Leest je toetsenbord en stuurt dat naar de hub | Enkel om in te stellen |

Zo werken ze samen:

```
WEDSTRIJD                                   UITZOEKEN / TESTEN

 main.py  (menu A, B, C...)                 computer               hub
   |                                        stuur_robot.py  ---->  vrij_rijden.py
   |  haalt de stappen uit                  (toetsenbord)  Bluetooth   |
   v                                                                   |
 missies.py  (MISSIE_A, MISSIE_B...)                                   |
   |                                                                   |
   |  alle drie gebruiken                                              |
   v                                                                   v
 supportcode.py  (motoren, veilig rijden, stappen uitvoeren)  <--------+
```

### Snel starten

**Op de wedstrijd:**
1. Zet `supportcode.py`, `missies.py` en `main.py` in Pybricks Code (allemaal in hetzelfde project).
2. Open `main.py` en druk op de startknop (Run).
3. Kies met LINKS/RECHTS een letter, start met de MIDDELSTE knop.

**Een afstand of hoek uitzoeken:** zie [vrij_rijden.py en stuur_robot.py](#vrij_rijdenpy-en-stuur_robotpy-rijden-met-het-toetsenbord).

**Na het uitzoeken: zet `main.py` terug op de hub voor de wedstrijd!**

---

## Deel 2: Uitleg per bestand

### supportcode.py: de gereedschapskist

Dit bestand voer je nooit zelf uit. Andere bestanden halen er hun onderdelen uit met `import`.

**1. Robot setup.** Hier staat hoe de robot gebouwd is:

| Naam | Poort | Wat |
|---|---|---|
| `Left_motor` | C | linker wiel |
| `Right_Motor` | D | rechter wiel |
| `LEFT_ATTACHMENT` | E | linker motor voor een opzetstuk |
| `RIGHT_ATTACHMENT` | F | rechter motor voor een opzetstuk |

- `WHEEL_DIAMETER = 62.4`: de diameter van een wiel in mm. Klopt dit niet, dan rijdt de robot te ver of niet ver genoeg.
- `AXLE_TRACK = 153`: de afstand tussen de twee wielen in mm. Klopt dit niet, dan draait de robot te veel of te weinig.
- `DRIVE_BASE`: combineert de twee wielmotoren tot één "rijdend onderstel". Daarmee kan je zeggen "rij 300 mm" in plaats van elke motor apart te sturen.

**2. Veiligheidsfuncties.** `safe_straight`, `safe_turn`, `safe_curve`, `safe_wait` en `safe_run_angle` doen hetzelfde als de gewone Pybricks-functies, maar kijken elke 10 milliseconden of je op de middelste knop drukt. Zo ja, dan roept `check_stop()` een `MissionStop` op: alle motoren stoppen, het lampje wordt rood en de hub piept.

**3. Menu.** `next_program` en `prior_program` gaan één stap vooruit of achteruit in de lijst van missies. Het teken `%` zorgt dat je na de laatste letter terug bij de eerste uitkomt.

**4. Snelheidsprofielen.**
- `set_precieze_modus()`: rustig rijden, gyro aan. Dit is de normale modus.
- `set_snelle_modus()`: zo snel mogelijk, gyro uit. Enkel om op het einde terug naar de basis te rijden.
- `start_missie()`: zet afstand en richting op 0 op de plek waar de robot nu staat. Dit gebeurt automatisch bij elke missie.

**5. Stappen-systeem.** `voer_stappen_uit(stappen)` loopt door de lijst van stappen uit `missies.py` en voert ze één voor één uit. Het nummer van de stap verschijnt op het scherm. Met `start_bij` en `eind_stap` kan je maar een stukje uitvoeren (dat gebruikt de testmodus).

**6. `safe_gyro_sprint`.** Een speciale functie om met volle kracht rechtdoor te rijden, met een eigen PID-regeling (zie [Deel 4](#deel-4-wat-is-pid)). Voor gewone missies gebruik je gewoon `("straight", ...)`.

### missies.py: hier schrijf jij de missies

Een missie is een **lijst van stappen**. Elke stap is een **tuple**: tussen haakjes, het eerste woord zegt *wat*, de getallen zeggen *hoeveel*.

```python
MISSIE_A = [
    ("straight", 300),                          # stap 0: 30 cm vooruit
    ("turn", 90),                               # stap 1: kwartdraai naar rechts
    ("run_angle", LEFT_ATTACHMENT, 200, 90),    # stap 2: linker arm 90 graden draaien
]
```

Alle soorten stappen:

| Stap | Betekenis | Voorbeeld |
|---|---|---|
| `("straight", mm)` | rechtdoor rijden, negatief is achteruit | `("straight", -150)` |
| `("turn", graden)` | ter plaatse draaien, positief is rechts, negatief is links | `("turn", -45)` |
| `("curve", straal, graden)` | een bocht rijden | `("curve", 200, 90)` |
| `("wait", ms)` | wachten (1000 ms = 1 seconde) | `("wait", 500)` |
| `("run_angle", motor, snelheid, graden)` | attachment draaien | `("run_angle", RIGHT_ATTACHMENT, 300, 180)` |
| `("run_angle", motor, snelheid, graden, Stop.COAST)` | idem, en daarna de motor loslaten | |
| `("snel",)` | vanaf nu snel rijden | |
| `("precies",)` | vanaf nu weer precies rijden | |
| `("gyro_uit",)` | gyro-correctie uit | |
| `("herhaal", aantal, [stappen])` | een reeks stappen herhalen | `("herhaal", 3, [("straight", 50), ("straight", -50)])` |
| `("call", functie)` | een eigen functie uitvoeren | `("call", stop_attachments)` |

Onderaan staat `MISSIE_STAPPEN`: een **dictionary** die elke letter van het menu koppelt aan een missie. Voeg je een missie F toe? Pas dan ook `PROGRAM_LIST` in `main.py` aan.

**Getallen met een naam.** Een getal dat je vaak bijstelt op de mat, krijgt bovenaan de missie een naam in HOOFDLETTERS, met de letter van de missie ervoor:

```python
A_AFSTAND_NAAR_BOOM = 250      # was 240

MISSIE_A = [
    ...
    ("straight", A_AFSTAND_NAAR_BOOM),
]
```

Zo pas je het getal op één plaats aan, en zie je in het commentaar wat de vorige waarde was.

**Eigen functies.** Moet de robot iets doen dat geen gewone stap is, schrijf dan een kleine functie met `def` en roep ze op met `("call", naam_van_de_functie)`. Let op: geen haakjes achter de naam, dus `("call", stop_attachments)` en niet `("call", stop_attachments())`.

#### Nieuwe missies schrijven

> **Nieuw seizoen!** De missies van vorig seizoen zijn verwijderd, want ze passen niet bij de mat van BIOGLOW Founders Edition. Alle missies A tot E zijn nu **leeg** en moeten nog geschreven worden. Wil je zien hoe de oude missies eruitzagen? Die staan nog in de geschiedenis op GitHub.

Zoek in `missies.py` naar **`NIEUWE STAPPEN HIER`**. Daar komen jullie stappen, telkens **boven** de regel `("call", stop_attachments)`: die moet altijd de laatste stap blijven, zodat de attachment-motoren na de missie loslaten.

```python
MISSIE_A = [
    # ---- NIEUWE STAPPEN HIER ----
    ("straight", 300),
    ("turn", 90),
    ("call", stop_attachments),   # laat deze regel altijd als LAATSTE staan
]
```

Schrijf ook bij elke missie in de titel welke missie van de mat het is, bijvoorbeeld `# MISSIE A: M03 (naam van de missie)`.

**Een extra missie toevoegen** (bijvoorbeeld F):
1. Kopieer in `missies.py` een volledig missieblok en noem het `MISSIE_F`.
2. Voeg in `MISSIE_STAPPEN` de regel `"F": MISSIE_F,` toe.
3. Voeg in `main.py` de letter `'F'` toe aan `PROGRAM_LIST`.

Onze missies (vul aan als een missie klaar is):

| Letter | Missie op de mat | Klaar? |
|---|---|---|
| A | nog te kiezen | nee |
| B | nog te kiezen | nee |
| C | nog te kiezen | nee |
| D | nog te kiezen | nee |
| E | nog te kiezen | nee |

### main.py: het wedstrijdprogramma

Dit programma toont een letter op het scherm van de hub. De knoppen:

| Knop | Wat gebeurt er? | Kleur lampje |
|---|---|---|
| LINKS / RECHTS | vorige / volgende missie | blauw |
| MIDDEN | missie starten (pas als je loslaat) | oranje tijdens het rijden |
| MIDDEN tijdens het rijden | noodstop | rood |
| LINKS + RECHTS samen | testmodus | |

Na een geslaagde missie springt het menu vanzelf naar de volgende letter.

**De testmodus** is er om niet telkens een hele missie te moeten rijden als je maar één stap wil controleren.

1. Lampje **geel**: kies met LINKS/RECHTS het nummer van de **startstap**, bevestig met MIDDEN.
2. Lampje **paars**: kies **hoeveel stappen** je wil testen, bevestig met MIDDEN.
3. De robot rijdt dat stukje (lampje oranje), daarna wordt het lampje **groen**:
   - MIDDEN kort: hetzelfde stukje nog eens
   - LINKS + RECHTS: een ander stukje kiezen
   - MIDDEN 1,5 seconde ingedrukt: testmodus verlaten

**Eén stap bijstellen:** kies je precies 1 stap en is dat een `straight` of `turn`, dan wordt het lampje **lichtblauw**. Met LINKS/RECHTS verander je de waarde telkens met 5, met MIDDEN probeer je het meteen. Dit verandert de code zelf **niet**: schrijf het getal op en pas het daarna aan in `missies.py`.

Zet de robot voor elke test met de hand terug op de juiste plek: de robot weet niet waar hij op de mat staat.

### vrij_rijden.py en stuur_robot.py: rijden met het toetsenbord

Hiermee rijd je de robot met de hand naar de juiste plek, en lees je af hoeveel mm en graden dat was. Die getallen gebruik je dan in `missies.py`.

**Eenmalig installeren op de computer** (in een terminal):

```
pip install bleak pynput
```

**Werkwijze:**
1. Open Pybricks Code, verbind met de hub en laad `vrij_rijden.py` op de hub.
2. Koppel Pybricks Code los van de hub (Bluetooth-icoontje).
3. Start op de computer: `python stuur_robot.py`
4. Verschijnt "Verbonden!"? Druk dan op de knop op de hub zelf om `vrij_rijden.py` te starten.

**Toetsen** (AZERTY):

| Toets | Actie |
|---|---|
| Z / S | vooruit / achteruit |
| Q / D | draaien links / rechts |
| I / K | linker attachment + / - |
| O / L | rechter attachment + / - |
| SHIFT ingedrukt | extra traag, voor de laatste millimeters |
| M | stapmodus aan/uit: elke tik is precies 5 mm of 1 graad |
| R | nulpunt: afstand, hoek en attachments hier op 0 zetten |
| SPATIE | toon een kant-en-klare regel om in `missies.py` te plakken |
| ESC | stoppen |
| knop op de hub | stopt altijd meteen |

Alles wat de hub terugstuurt wordt ook bewaard in `rijlog.txt` op de computer.

**Tip:** de getallen die je met SPATIE krijgt tellen vanaf het laatste nulpunt. Werk daarom per stukje: rij rechtdoor, druk SPATIE, druk R, draai, druk SPATIE, druk R, ...

**Veiligheid:** komt er 0,5 seconde lang niets binnen van de computer (verbinding weg), dan stopt de robot vanzelf.

**Instellingen** staan bovenaan `vrij_rijden.py`: snelheden, stapgrootte en de PID-waarden. Met `GEBRUIK_EIGEN_PID = False` gebruik je de ingebouwde gyroregeling van Pybricks in plaats van onze eigen PID. Probeer beide en kies wat het rechtst rijdt.

Heet jullie hub anders dan `githo botic`? Pas dan `HUB_NAME` bovenaan `stuur_robot.py` aan.

**Na het uitzoeken: zet `main.py` terug op de hub voor de wedstrijd!**

---

## Deel 3: Python basis

Hier staat alles wat je nodig hebt om onze code te lezen. Probeer de voorbeelden zelf uit!

### 3.1 Commentaar

Alles achter een `#` is **commentaar**: uitleg voor mensen. De computer slaat het over.

```python
# Dit is commentaar
afstand = 300   # ook hier mag commentaar staan
```

Tekst tussen drie aanhalingstekens `"""..."""` bovenaan een functie heet een **docstring**: de uitleg van wat die functie doet.

### 3.2 Variabelen

Een **variabele** is een doosje met een naam waar je iets in bewaart. Met `=` stop je er iets in.

```python
snelheid = 120
snelheid = snelheid + 10   # nu zit er 130 in
```

Namen in **HOOFDLETTERS** (zoals `WHEEL_DIAMETER` of `RIJSNELHEID`) zijn bij afspraak **instellingen**: waarden die je bovenaan een bestand aanpast, maar die tijdens het programma niet veranderen.

### 3.3 Soorten gegevens

| Soort | Voorbeeld | Uitleg |
|---|---|---|
| geheel getal (`int`) | `300`, `-90` | |
| kommagetal (`float`) | `62.4` | Let op: een **punt**, geen komma! |
| tekst (`str`) | `"straight"` | altijd tussen aanhalingstekens |
| waar/onwaar (`bool`) | `True`, `False` | met een hoofdletter |
| niets | `None` | "er is (nog) geen waarde" |

### 3.4 Rekenen en vergelijken

```python
a = 7 + 3     # 10
b = 7 - 3     # 4
c = 7 * 3     # 21
d = 7 / 2     # 3.5
e = 7 % 3     # 1  (de rest bij delen: 7 = 2*3 + 1)
a += 5        # kort voor: a = a + 5
```

Vergelijken geeft `True` of `False`:

| Teken | Betekenis |
|---|---|
| `==` | is gelijk aan (twee =-tekens! één = is "stop in de variabele") |
| `!=` | is niet gelijk aan |
| `<`, `>` | kleiner dan, groter dan |
| `<=`, `>=` | kleiner of gelijk, groter of gelijk |
| `and`, `or`, `not` | en, of, niet |
| `in` | zit erin? (bv. `Button.CENTER in pressed`) |

### 3.5 Inspringen (heel belangrijk!)

Python gebruikt **inspringen** (4 spaties) om te tonen welke regels bij elkaar horen. Een regel die eindigt op een **dubbelpunt** `:` wordt altijd gevolgd door ingesprongen regels.

```python
if afstand > 100:
    print("ver")      # hoort bij de if
    print("echt ver") # hoort ook bij de if
print("klaar")        # hoort er niet meer bij, gebeurt altijd
```

### 3.6 Als ... dan ... anders: `if`, `elif`, `else`

```python
if Button.LEFT in pressed:
    print("links")
elif Button.RIGHT in pressed:     # elif = "anders, als ..."
    print("rechts")
else:                              # in alle andere gevallen
    print("geen knop")
```

Python controleert van boven naar onder en voert **enkel het eerste** blok uit dat klopt.

### 3.7 Herhalen: `while` en `for`

`while` herhaalt **zolang** iets waar is. `while True:` herhaalt voor altijd (tot `break` of `return`).

```python
teller = 0
while teller < 3:
    print(teller)      # toont 0, 1, 2
    teller += 1
```

`for` gaat **elk element** van een lijst af:

```python
for stap in MISSIE_A:
    print(stap)

for i in range(3):     # range(3) geeft 0, 1, 2
    print(i)

for i, stap in enumerate(MISSIE_A):   # i is het nummer, stap is de stap zelf
    print(i, stap)
```

- `break`: stop meteen met de lus.
- `continue`: sla de rest over en ga verder met de volgende ronde.

### 3.8 Lijsten en tuples

Een **lijst** staat tussen vierkante haken `[ ]` en kan je aanpassen. Een **tuple** staat tussen ronde haken `( )` en ligt vast. Je telt **vanaf 0**!

```python
letters = ['A', 'B', 'C']
letters[0]        # 'A'  (het eerste element)
letters[2]        # 'C'
len(letters)      # 3    (hoeveel elementen)

stap = ("straight", 300)
stap[0]           # "straight"
stap[1]           # 300
```

Een tuple met maar één element heeft een komma nodig: `("snel",)`.

### 3.9 Dictionaries

Een **dictionary** (woordenboek) koppelt een **sleutel** aan een **waarde**, tussen accolades `{ }`.

```python
MISSIE_STAPPEN = {
    "A": MISSIE_A,
    "B": MISSIE_B,
}
MISSIE_STAPPEN["A"]    # geeft de lijst MISSIE_A
```

### 3.10 Functies

Een **functie** is een stukje code met een naam, dat je opnieuw kan gebruiken. Je maakt ze met `def`. Tussen de haakjes staan de **parameters**: de dingen die je meegeeft.

```python
def dubbel(getal):
    return getal * 2     # return geeft een antwoord terug

x = dubbel(5)            # x is nu 10
```

Een parameter kan een **standaardwaarde** hebben. Geef je niets mee, dan wordt die gebruikt:

```python
def voer_stappen_uit(stappen, start_bij=0, eind_stap=None):
    ...

voer_stappen_uit(MISSIE_A)                 # start_bij is 0
voer_stappen_uit(MISSIE_A, start_bij=3)    # start bij stap 3
```

### 3.11 Methoden: de punt

Met een **punt** vraag je iets aan een object. Lees `DRIVE_BASE.straight(300)` als "DRIVE_BASE, rij 300 mm rechtdoor".

```python
HUB.light.on(Color.RED)          # hub, lampje, ga aan in het rood
HUB.speaker.beep(600, 100)       # hub, luidspreker, piep 600 Hz gedurende 100 ms
LEFT_ATTACHMENT.angle()          # linker attachment, wat is je hoek?
```

### 3.12 Importeren

Met `import` haal je code uit een ander bestand.

```python
from supportcode import DRIVE_BASE, HUB    # enkel deze twee
from supportcode import *                  # alles uit supportcode.py
```

Alle bestanden met `from pybricks...` komen uit Pybricks zelf.

### 3.13 Fouten opvangen: `try` en `except`

Zo werkt onze noodstop. Gaat er iets "mis" in het `try`-blok (bijvoorbeeld de knop wordt ingedrukt en `check_stop()` roept `MissionStop` op), dan springt Python meteen naar het `except`-blok.

```python
try:
    voer_stappen_uit(MISSIE_A)
    HUB.speaker.beep(600, 100)       # gelukt!
except MissionStop:
    DRIVE_BASE.stop()                # gestopt met de knop
```

### 3.14 `global`

Een variabele die je **binnen** een functie verandert, bestaat normaal enkel binnen die functie. Met `global naam` zeg je: "ik bedoel de variabele van buiten de functie". Dat zie je in `stuur_robot.py`.

### 3.15 Veelgemaakte fouten

| Foutmelding | Oorzaak |
|---|---|
| `IndentationError` | inspringen klopt niet (mix van spaties en tabs, of vergeten in te springen) |
| `SyntaxError` | vergeten `:` na `if`/`while`/`def`, vergeten komma in een lijst, haakje niet gesloten |
| `NameError` | naam verkeerd geschreven (Python let op hoofdletters: `Hub` is niet `HUB`) |
| `KeyError: 'F'` | letter staat in `PROGRAM_LIST` maar niet in `MISSIE_STAPPEN` |
| `IndexError` | je vraagt een element dat niet bestaat, bv. `letters[5]` als er maar 3 zijn |
| `TypeError` | een stap heeft te weinig of te veel getallen |

---

## Deel 4: Wat is PID?

De robot rijdt nooit perfect recht: een wiel slipt een beetje, de mat is niet vlak... De **gyro** in de hub meet in welke richting de robot kijkt. **PID** is een slimme manier om bij te sturen.

Stel: de robot moet naar 0 graden kijken, maar kijkt naar 3 graden. De **fout** is dan 3 graden.

- **P (proportioneel):** hoe groter de fout, hoe harder bijsturen. Te groot: de robot zigzagt. Te klein: hij stuurt te traag bij.
- **I (integraal):** telt kleine fouten op die maar blijven hangen, en werkt die zo toch weg.
- **D (afgeleide):** kijkt hoe snel de fout verandert en remt de bijsturing af, zodat de robot niet doorschiet.

```
correctie = KP * fout + KI * opgetelde_fout + KD * verandering_van_de_fout
```

Instellen doe je door te proberen: begin met enkel P, zet I en D op 0. Verhoog P tot de robot begint te zigzaggen en neem dan iets minder. Voeg daarna een beetje D toe tegen het zigzaggen, en een beetje I als hij steeds net naast de lijn eindigt.

---

## Woordenlijst

| Woord | Betekenis |
|---|---|
| hub | het grote LEGO blok met scherm en knoppen: de computer van de robot |
| poort | aansluiting op de hub (A tot F) |
| attachment | opzetstuk op de robot, bv. een arm of grijper |
| gyro / IMU | sensor in de hub die meet hoe de robot gedraaid is |
| heading | de richting waarin de robot kijkt, in graden |
| DriveBase | Pybricks-object dat twee wielen samen laat rijden |
| Pybricks | de software waarmee we de LEGO hub in Python programmeren |
| BLE | Bluetooth Low Energy: draadloze verbinding tussen computer en hub |
| ms | milliseconde, 1000 ms = 1 seconde |
| duty cycle (dc) | hoeveel procent van zijn kracht een motor krijgt |

---

## Afspraken als je code aanpast

1. **Zet uitleg bij elke aanpassing**, als commentaar in de code. Schrijf het zo dat iemand uit het 2de middelbaar zonder Python-kennis het begrijpt.
2. **Pas deze README aan** als je iets verandert dat hier beschreven staat (nieuwe staptypes, andere knoppen, andere poorten, ...).
3. Instellingen (snelheden, poorten, PID-waarden) staan altijd **bovenaan** het bestand in HOOFDLETTERS. Pas ze daar aan, nergens anders.
4. Test een aanpassing eerst met de testmodus voor je een hele missie rijdt.
