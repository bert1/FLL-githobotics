# FLL-githobotics

Welkom! Dit is de code van onze robot voor de **FIRST LEGO League**, seizoen **BIOGLOW Founders Edition**. We programmeren de LEGO hub in Python met **Pybricks**.

Nog nooit met GitHub of Python gewerkt? Geen probleem: volg de stappen hieronder in volgorde.

## Code op de robot zetten

| Wat wil je doen? | Download | Uitleg |
|---|---|---|
| De **eerste keer** alles op de robot zetten | **[robot-volledig.zip](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/robot-volledig.zip)** | [stappenplan](docs/1-github-en-pybricks.md#de-eerste-keer-alles-op-de-robot-zetten) |
| **Bijwerken** naar een nieuwe versie (je eigen missies blijven) | **[robot-zonder-missies.zip](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/robot-zonder-missies.zip)** | [stappenplan](docs/1-github-en-pybricks.md#er-is-een-nieuwe-versie-bijwerken) |
| De robot **besturen met het toetsenbord** en je missie **opnemen** (op een Windows-computer, niets te installeren) | **[stuur_robot.exe](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/stuur_robot.exe)** | [uitleg](docs/4-uitleg-code.md#vrij_rijdenpy-en-stuur_robotpy-rijden-met-het-toetsenbord) |
| Hetzelfde op een **Mac** (Python nodig) | **[stuur_robot.py](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/stuur_robot.py)** | [uitleg](docs/4-uitleg-code.md#op-een-mac-of-linux-met-python) |

In Pybricks Code ([code.pybricks.com](https://code.pybricks.com)) klik je op **Import a file** en kies je het ZIP-bestand. Je hoeft het niet uit te pakken.

Wat er in elke versie veranderd is, lees je in **[WIJZIGINGEN.md](WIJZIGINGEN.md)**.

## Uitleg: lees in deze volgorde

1. **[GitHub en Pybricks](docs/1-github-en-pybricks.md)**: wat is GitHub, hoe download je de code en hoe zet je ze in Pybricks Code.
2. **[Python basis](docs/2-python-basis.md)**: alles wat je over Python moet weten om onze code te lezen.
3. **[Missies schrijven](docs/3-missies-schrijven.md)**: hier begin je als je de robot iets wil laten doen op de mat.
4. **[Uitleg van de code](docs/4-uitleg-code.md)**: wat elk bestand doet, de knoppen op de hub, de testmodus en rijden met het toetsenbord.

## Wat staat waar?

| Map of bestand | Wat zit erin? |
|---|---|
| [`robot/`](robot) | de code voor de **hub**. Deze bestanden gaan naar Pybricks Code. |
| [`robot/missies.py`](robot/missies.py) | **de missies: hier werken jullie het meest in** |
| [`robot/main.py`](robot/main.py) | het wedstrijdprogramma: menu om missies te kiezen, te testen en (letter V) met het toetsenbord te rijden |
| [`robot/supportcode.py`](robot/supportcode.py) | instellingen van de robot (poorten, wielmaat) en alle hulpfuncties |
| [`robot/vrij_rijden.py`](robot/vrij_rijden.py) | de robot laten rijden met het toetsenbord en alles opnemen als stappen |
| [`computer/stuur_robot.py`](computer/stuur_robot.py) | draait op de **computer**: leest het toetsenbord, stuurt dat naar de hub en schrijft de opname in `opname.txt` (en alle opnames in `alle_opnames.txt`). Met C kopieer je de stappen. |
| [`docs/`](docs) | alle uitleg |
| [`WIJZIGINGEN.md`](WIJZIGINGEN.md) | wat er in elke versie veranderd is |

Zo werken de bestanden samen:

```
            HUB                                            COMPUTER

 main.py  (menu A, B, C... en V)
   |                 |
   |  haalt de       |  letter V: rijden met     Bluetooth
   |  stappen uit    +-------> vrij_rijden.py  <---------->  stuur_robot.py
   v                                 |                       (toetsenbord)
 missies.py  (MISSIE_A...)           |                            |
   |                                 |                            v
   |  allemaal gebruiken             |                       opname.txt
   v                                 v                       (stappen om te plakken)
 supportcode.py  (motoren, veilig rijden, stappen uitvoeren)
```

## Afspraken als je code aanpast

1. **Zet uitleg bij elke aanpassing**, als commentaar in de code. Schrijf het zo dat iemand uit het 2de middelbaar zonder Python-kennis het begrijpt.
2. **Pas de uitleg in `docs/` aan** als je iets verandert dat daar beschreven staat (nieuwe staptypes, andere knoppen, andere poorten, ...).
3. **Schrijf in [WIJZIGINGEN.md](WIJZIGINGEN.md)** wat er veranderd is, zet `VERSIE` bovenaan `robot/supportcode.py` op de datum van vandaag, en zeg of `missies.py` mee aangepast moet worden.
4. Instellingen (snelheden, poorten, PID-waarden) staan altijd **bovenaan** het bestand in HOOFDLETTERS. Pas ze daar aan, nergens anders.
5. Test een aanpassing eerst met de testmodus voor je een hele missie rijdt.
