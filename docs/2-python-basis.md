# 2. Python basis

Hier staat alles wat je nodig hebt om onze code te lezen. Probeer de voorbeelden zelf uit!

## 1. Commentaar

Alles achter een `#` is **commentaar**: uitleg voor mensen. De computer slaat het over.

```python
# Dit is commentaar
afstand = 300   # ook hier mag commentaar staan
```

Tekst tussen drie aanhalingstekens `"""..."""` bovenaan een functie heet een **docstring**: de uitleg van wat die functie doet.

## 2. Variabelen

Een **variabele** is een doosje met een naam waar je iets in bewaart. Met `=` stop je er iets in.

```python
snelheid = 120
snelheid = snelheid + 10   # nu zit er 130 in
```

Namen in **HOOFDLETTERS** (zoals `WHEEL_DIAMETER` of `RIJSNELHEID`) zijn bij afspraak **instellingen**: waarden die je bovenaan een bestand aanpast, maar die tijdens het programma niet veranderen.

## 3. Soorten gegevens

| Soort | Voorbeeld | Uitleg |
|---|---|---|
| geheel getal (`int`) | `300`, `-90` | |
| kommagetal (`float`) | `62.4` | Let op: een **punt**, geen komma! |
| tekst (`str`) | `"straight"` | altijd tussen aanhalingstekens |
| waar/onwaar (`bool`) | `True`, `False` | met een hoofdletter |
| niets | `None` | "er is (nog) geen waarde" |

## 4. Rekenen en vergelijken

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

## 5. Inspringen (heel belangrijk!)

Python gebruikt **inspringen** (4 spaties) om te tonen welke regels bij elkaar horen. Een regel die eindigt op een **dubbelpunt** `:` wordt altijd gevolgd door ingesprongen regels.

```python
if afstand > 100:
    print("ver")      # hoort bij de if
    print("echt ver") # hoort ook bij de if
print("klaar")        # hoort er niet meer bij, gebeurt altijd
```

## 6. Als ... dan ... anders: `if`, `elif`, `else`

```python
if Button.LEFT in pressed:
    print("links")
elif Button.RIGHT in pressed:     # elif = "anders, als ..."
    print("rechts")
else:                              # in alle andere gevallen
    print("geen knop")
```

Python controleert van boven naar onder en voert **enkel het eerste** blok uit dat klopt.

## 7. Herhalen: `while` en `for`

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

## 8. Lijsten en tuples

Een **lijst** staat tussen vierkante haken `[ ]` en kan je aanpassen. Een **tuple** staat tussen ronde haken `( )` en ligt vast. Je telt **vanaf 0**!

```python
letters = ['A', 'B', 'C']
letters[0]        # 'A'  (het eerste element)
letters[2]        # 'C'
letters[-1]       # 'C'  (negatief telt van achteren: -1 is het laatste element)
len(letters)      # 3    (hoeveel elementen)

stap = ("straight", 300)
stap[0]           # "straight"
stap[1]           # 300
```

Een tuple met maar één element heeft een komma nodig: `("snel",)`.

Een lijst aanpassen (dat kan niet met een tuple):

```python
opname = []                       # een lege lijst
opname.append(("straight", 412))  # achteraan iets toevoegen
laatste = opname.pop()            # het laatste element eruit halen
opname.clear()                    # de lijst helemaal leeg maken
['A', 'B'] + ['V']                # twee lijsten aan elkaar: ['A', 'B', 'V']
```

Een **stuk** van een lijst of tuple nemen doe je met een dubbelpunt:

```python
stap = ("run_angle", LEFT_ATTACHMENT, 200, 90)
stap[1:]          # alles vanaf element 1: (LEFT_ATTACHMENT, 200, 90)
stap[0:2]         # element 0 en 1 (2 niet meer): ("run_angle", LEFT_ATTACHMENT)
```

## 9. Dictionaries

Een **dictionary** (woordenboek) koppelt een **sleutel** aan een **waarde**, tussen accolades `{ }`.

```python
MISSIE_STAPPEN = {
    "A": MISSIE_A,
    "B": MISSIE_B,
}
MISSIE_STAPPEN["A"]    # geeft de lijst MISSIE_A
```

## 10. Functies

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

## 11. Methoden: de punt

Met een **punt** vraag je iets aan een object. Lees `DRIVE_BASE.straight(300)` als "DRIVE_BASE, rij 300 mm rechtdoor".

```python
HUB.light.on(Color.RED)          # hub, lampje, ga aan in het rood
HUB.speaker.beep(600, 100)       # hub, luidspreker, piep 600 Hz gedurende 100 ms
LEFT_ATTACHMENT.angle()          # linker attachment, wat is je hoek?
```

## 12. Importeren

Met `import` haal je code uit een ander bestand.

```python
from supportcode import DRIVE_BASE, HUB    # enkel deze twee
from supportcode import *                  # alles uit supportcode.py
```

Alle bestanden met `from pybricks...` komen uit Pybricks zelf.

Bij `import` voert Python het hele andere bestand uit. Soms mag een stuk daarvan enkel lopen als je dat bestand **zelf** start. Dat zie je onderaan `vrij_rijden.py`:

```python
if __name__ == "__main__":
    vrij_rijden()
```

`__name__` is de naam van het bestand dat nu loopt. Start je `vrij_rijden.py` zelf, dan is die naam `"__main__"` en begint het rijden meteen. Haalt `main.py` het op met `import`, dan niet: dan start het rijden pas als je in het menu V kiest.

## 13. Fouten opvangen: `try` en `except`

Zo werkt onze noodstop. Gaat er iets "mis" in het `try`-blok (bijvoorbeeld de knop wordt ingedrukt en `check_stop()` roept `MissionStop` op), dan springt Python meteen naar het `except`-blok.

```python
try:
    voer_stappen_uit(MISSIE_A)
    HUB.speaker.beep(600, 100)       # gelukt!
except MissionStop:
    DRIVE_BASE.stop()                # gestopt met de knop
```

## 14. `global`

Een variabele die je **binnen** een functie verandert, bestaat normaal enkel binnen die functie. Met `global naam` zeg je: "ik bedoel de variabele van buiten de functie". Dat zie je in `stuur_robot.py`.

In `stuur_robot.py` staat ook `getattr(sys, "frozen", False)`. Dat betekent: "geef de waarde `sys.frozen`, en bestaat die niet, geef dan `False`". `sys.frozen` bestaat enkel als het programma als `stuur_robot.exe` draait. Zo weet het programma of iemand op de `.exe` dubbelklikte.

Met `"--controle" in sys.argv` kijk je of het programma gestart werd met het woord `--controle` erachter (`sys.argv` is de lijst met alles wat achter de naam van het programma getypt werd).

## 15. Veelgemaakte fouten

| Foutmelding | Oorzaak |
|---|---|
| `IndentationError` | inspringen klopt niet (mix van spaties en tabs, of vergeten in te springen) |
| `SyntaxError` | vergeten `:` na `if`/`while`/`def`, vergeten komma in een lijst, haakje niet gesloten |
| `NameError` | naam verkeerd geschreven (Python let op hoofdletters: `Hub` is niet `HUB`) |
| `IndexError` | je vraagt een element dat niet bestaat, bv. `letters[5]` als er maar 3 zijn |
| `TypeError` | een waarde van de verkeerde soort, bv. tekst waar een getal moet |

Fouten **in een stap** van een missie (tikfout, getal vergeten, komma vergeten) vangt `main.py` zelf op bij het opstarten: rood lampje en uitleg in Pybricks Code. Zie [Missies schrijven](3-missies-schrijven.md#tikfout-in-een-missie).

## 16. Handige ingebouwde functies

Deze functies zitten in Python zelf, je hoeft ze niet te importeren.

| Functie | Wat doet ze? | Voorbeeld |
|---|---|---|
| `print(...)` | tekst tonen (in Pybricks Code onderaan) | `print("klaar")` |
| `len(x)` | hoeveel elementen | `len(MISSIE_A)` |
| `abs(x)` | getal zonder minteken | `abs(-5)` is `5` |
| `round(x)` | afronden | `round(2.7)` is `3` |
| `str(x)` | getal omzetten naar tekst | `"stap " + str(4)` is `"stap 4"` |
| `sorted(x)` | in volgorde zetten | `sorted(["C", "A", "B"])` is `["A", "B", "C"]` |
| `isinstance(x, soort)` | is x van deze soort? | `isinstance(300, int)` is `True` |
| `callable(x)` | is x een functie die je kan uitvoeren? | `callable(stop_attachments)` is `True` |
| `chr(x)` | het teken dat bij een codenummer hoort | `chr(50)` is `"2"` |

**Leeg telt als False.** Een lege lijst `[]`, een lege dictionary `{}`, een lege verzameling, `0` en `None` tellen in een `if` of `while` als `False`. Daarom werkt `while HUB.buttons.pressed():` als "zolang er een knop ingedrukt is".
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

---

[Terug naar de startpagina](../README.md)
