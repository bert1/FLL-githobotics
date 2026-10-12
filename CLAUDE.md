# Afspraken voor dit project

Dit is FLL-code (FIRST LEGO League, seizoen BIOGLOW Founders Edition) in Pybricks
MicroPython, geschreven door en voor leerlingen van het 2de middelbaar die Python
nog aan het leren zijn.

- Elke aanpassing aan de code krijgt uitleg als commentaar in het Nederlands,
  begrijpelijk voor een leerling van het 2de middelbaar zonder Python-kennis.
  Markeer een gewijzigd stuk met `# AANGEPAST:` en leg uit wat er veranderde en waarom.
- Pas de uitleg (README.md en docs/) altijd mee aan wanneer de code verandert (bestanden, staptypes,
  knoppen, toetsen, poorten, instellingen). Ook het deel "Python basis" als er
  nieuwe Python-concepten in de code komen.
- Gebruik geen gedachtestreep (het lange streepje) in Nederlandse tekst.
- "githo nijlen" schrijf je altijd zonder hoofdletters.
- robot/ (supportcode.py, missies.py, main.py, vrij_rijden.py) draait op de hub
  (Pybricks MicroPython, geen gewone Python-bibliotheken). computer/stuur_robot.py
  draait op de computer (gewone Python, met bleak, pynput en rich).
- De leerlingen kennen GitHub niet. Ze downloaden de ZIP-bestanden van de release
  "nieuwste" (gemaakt door .github/workflows/maak-downloads.yml) en importeren
  die in Pybricks Code. Houd die werkwijze eenvoudig en de links in README.md en
  docs/1-github-en-pybricks.md geldig.
- Bij elke codewijziging: VERSIE bovenaan robot/supportcode.py op de datum van
  vandaag zetten, en bovenaan WIJZIGINGEN.md een nieuw blok toevoegen met wat er
  veranderd is (in leerlingentaal), welke bestanden, en of missies.py mee moet
  veranderen. missies.py bevat het werk van de leerlingen: geef in dat geval
  precies aan wat ze zelf moeten aanpassen, zodat ze hun missies niet verliezen.
- De uitleg staat in docs/ (1 GitHub en Pybricks, 2 Python basis, 3 Missies
  schrijven, 4 Uitleg van de code). README.md is de startpagina.
