# 3. Missies schrijven

Alle missies staan in het bestand `robot/missies.py`. Dit is het bestand waar jullie het meest in werken.

> **Nieuw seizoen!** De missies van vorig seizoen zijn verwijderd, want ze passen niet bij de mat van BIOGLOW Founders Edition. Alle missies A tot E zijn nu **leeg** en moeten nog geschreven worden. Wil je zien hoe de oude missies eruitzagen? Die staan nog in de geschiedenis op GitHub (zie [1. GitHub en Pybricks](1-github-en-pybricks.md#een-oudere-versie-bekijken)).

**Inhoud**
- [Hoe ziet een missie eruit?](#hoe-ziet-een-missie-eruit)
- [Alle soorten stappen](#alle-soorten-stappen)
- [Waar schrijf je een nieuwe missie?](#waar-schrijf-je-een-nieuwe-missie)
- [Handige tips](#handige-tips)
- [Tikfout in een missie?](#tikfout-in-een-missie)
- [Je missies bewaren](#je-missies-bewaren)
- [Onze missies](#onze-missies)

## Hoe ziet een missie eruit?

Een missie is een **lijst van stappen**. Elke stap is een **tuple**: tussen haakjes, het eerste woord zegt *wat*, de getallen zeggen *hoeveel*.

```python
MISSIE_A = [
    ("straight", 300),                          # stap 0: 30 cm vooruit
    ("turn", 90),                               # stap 1: kwartdraai naar rechts
    ("run_angle", LEFT_ATTACHMENT, 200, 90),    # stap 2: linker arm 90 graden draaien
    ("call", stop_attachments),                 # stap 3: altijd als laatste
]
```

De stappen tellen **vanaf 0**. Dat nummer zie je op het scherm van de hub tijdens het rijden, en dat nummer kies je in de testmodus.

## Alle soorten stappen

| Stap | Betekenis | Voorbeeld |
|---|---|---|
| `("straight", mm)` | rechtdoor rijden, negatief is achteruit | `("straight", -150)` |
| `("turn", graden)` | ter plaatse draaien, positief is rechts, negatief is links | `("turn", -45)` |
| `("curve", straal, graden)` | een bocht rijden. Straal positief = vooruit, negatief = achteruit. Graden positief = naar rechts (als je vooruit rijdt) | `("curve", 200, 90)` |
| `("wait", ms)` | wachten (1000 ms = 1 seconde) | `("wait", 500)` |
| `("run_angle", motor, snelheid, graden)` | attachment draaien | `("run_angle", RIGHT_ATTACHMENT, 300, 180)` |
| `("run_angle", motor, snelheid, graden, Stop.COAST)` | idem, en daarna de motor loslaten | |
| `("snel",)` | vanaf nu snel rijden | |
| `("precies",)` | vanaf nu weer precies rijden | |
| `("gyro_uit",)` | gyro-correctie uit | |
| `("herhaal", aantal, [stappen])` | een reeks stappen herhalen | `("herhaal", 3, [("straight", 50), ("straight", -50)])` |
| `("call", functie)` | een eigen functie uitvoeren | `("call", stop_attachments)` |

Let op: een stap met maar één woord heeft toch een komma nodig: `("snel",)` is goed, `("snel")` is fout.

## Waar schrijf je een nieuwe missie?

Zoek in `missies.py` naar **`NIEUWE STAPPEN HIER`**. Daar komen jullie stappen, telkens **boven** de regel `("call", stop_attachments)`. Die moet altijd de laatste stap blijven, zodat de attachment-motoren na de missie loslaten.

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
2. Voeg onderaan in `MISSIE_STAPPEN` de regel `"F": MISSIE_F,` toe.

Meer hoeft niet: het menu in `main.py` neemt de letter F vanzelf over.

## Handige tips

**Een missie opnemen.** Je hoeft niet te gokken hoeveel mm de robot moet rijden. Kies in het menu de letter V en rij met het toetsenbord de hele missie. Elke beweging wordt een stap, en alle stappen staan klaar in `opname.txt` op de computer. Die plak je zo in je missie. Met P speel je alles meteen af op wedstrijdsnelheid. Zie [vrij_rijden.py en stuur_robot.py](4-uitleg-code.md#vrij_rijdenpy-en-stuur_robotpy-rijden-met-het-toetsenbord).

**Het volgende stuk van een missie opnemen.** Laat de robot in de testmodus het begin van de missie rijden en druk daarna RECHTS: je rijdt verder met het toetsenbord, vanaf de plek waar de missie eindigt. Zie [Verder vanaf een missie](4-uitleg-code.md#verder-vanaf-een-missie).

**Een stukje testen.** Druk in het menu LINKS en RECHTS samen in voor de testmodus. Dan rijdt de robot maar een paar stappen. Zie [de testmodus](4-uitleg-code.md#mainpy-het-wedstrijdprogramma).

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

## Tikfout in een missie?

Bij het opstarten kijkt `main.py` alle missies na. Vindt het een fout, dan:
- wordt het lampje **rood**,
- loopt de letter en het stapnummer over het scherm, bijvoorbeeld `B 4` (missie B, stap 4),
- staat de uitleg onderaan in Pybricks Code, bijvoorbeeld `FOUT in missie B stap 4 : onbekende soort stap 'stright'. Tikfout?`

Een missie met een fout kan je niet starten en niet testen: het lampje blijft rood als je die letter kiest. De andere missies werken gewoon, zodat je op de wedstrijd nooit vastzit door één foute missie.

## Je missies bewaren

Jullie missies staan in Pybricks Code, in de browser van de computer waarop je werkt. Wis je de browsergegevens of werk je op een andere computer, dan zijn ze weg. Daarom:

1. **Maak na elke sessie een back-up** in Pybricks Code (zie [1. GitHub en Pybricks](1-github-en-pybricks.md#een-back-up-maken-in-pybricks-code)).
2. **Bezorg je `missies.py` aan de coach**, zodat die ze op GitHub kan zetten. Dan heeft het hele team altijd de nieuwste missies.

## Onze missies

Vul aan als een missie klaar is:

| Letter | Missie op de mat | Klaar? |
|---|---|---|
| A | nog te kiezen | nee |
| B | nog te kiezen | nee |
| C | nog te kiezen | nee |
| D | nog te kiezen | nee |
| E | nog te kiezen | nee |

---

[Terug naar de startpagina](../README.md)
