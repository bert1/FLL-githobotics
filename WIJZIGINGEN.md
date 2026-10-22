# Wijzigingen

Hier staat bij elke nieuwe versie wat er veranderd is, en wat jij moet doen om bij te werken.
De nieuwste versie staat altijd bovenaan.

Welke versie staat er op jullie robot? Start `main.py` in Pybricks Code. Onderaan verschijnt bijvoorbeeld `githobotics code versie 2026-10-12`.

Hoe werk je bij? Zie [1. GitHub en Pybricks](docs/1-github-en-pybricks.md#er-is-een-nieuwe-versie-bijwerken).

---

## Versie 2026-10-22b

De robot reed nog door na het loslaten van een toets, en hij stuurde nog te vroeg bij.

**Wat moet je doen?**
- Download [robot-zonder-missies.zip](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/robot-zonder-missies.zip) en importeer het in Pybricks Code. Kies telkens voor vervangen.
- Download ook de nieuwe **[stuur_robot.exe](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/stuur_robot.exe)** (of op een Mac [stuur_robot.py](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/stuur_robot.py)).
- Zegt Pybricks Code *"Werk de Pybricks-firmware bij, dan stopt de robot sneller"*? Installeer dan de nieuwste firmware op de hub (in Pybricks Code, via het tandwiel).
- **`missies.py` hoeft niet te veranderen.** Jullie missies blijven zoals ze zijn.

**Wat is er nieuw?**
- **Meteen stoppen:** laat je een toets los, dan remt de robot nu hard (`RIJ_AFREMMEN`, `DRAAI_AFREMMEN`). Vertrekken blijft zacht.
- **Sneller doorgeven:** de computer stuurt een ingedrukte of losgelaten toets meteen naar de hub, in plaats van eerst even te wachten.
- **Attachments** draaien trager (100 in plaats van 150 graden per seconde), zodat ze minder ver doorschieten.
- **Gyro langer uit:** na het rustig vertrekken rijdt de robot nog anderhalve seconde zonder gyro (`GYRO_WACHTTIJD`). Daarna stuurt de gyro bij, eerst heel zacht (`GYRO_INLOOPTIJD`). Schommelt hij nog? Zet `GYRO_WACHTTIJD` bovenaan `vrij_rijden.py` hoger.

**Welke bestanden?** `robot/vrij_rijden.py`, `computer/stuur_robot.py`, `robot/supportcode.py` (enkel `VERSIE`) en de uitleg.

---

## Versie 2026-10-22

Jullie opmerkingen over rijden met het toetsenbord zijn verwerkt: makkelijker kopiëren, geen rare kleine stappen meer, en de robot rijdt rustiger.

**Wat moet je doen?**
- Maak eerst een back-up in Pybricks Code (**Backup all files**).
- Download [robot-zonder-missies.zip](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/robot-zonder-missies.zip) en importeer het in Pybricks Code. Kies telkens voor vervangen.
- Download ook de nieuwe **[stuur_robot.exe](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/stuur_robot.exe)** (of op een Mac [stuur_robot.py](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/stuur_robot.py)) en zet die in de plaats van de oude.
- Het oude bestand `rijlog.txt` wordt niet meer gebruikt. Je mag het weggooien.
- **`missies.py` hoeft niet te veranderen.** Jullie missies blijven zoals ze zijn.

**Wat is er nieuw?**
- **Kopiëren met C:** druk C en alle stappen staan op het klembord. Plak ze met CTRL+V in `missies.py`. Na het stoppen (ESC) gebeurt dat vanzelf. Je hoeft niets meer te selecteren in het zwarte venster.
- Na het stoppen staan de stappen in het venster **zonder kader** eromheen, zodat je ook daar netjes kan selecteren.
- **alle_opnames.txt** in plaats van `rijlog.txt`: elke afgewerkte opname komt erin, de **nieuwste bovenaan**. Geen tijdstip meer voor elke regel, en stappen die je met BACKSPACE wiste, staan er **niet** meer in.
- **Rechtdoor blijft rechtdoor:** Z of S wordt nu altijd een `"straight"`, ook als de robot onderweg een beetje afwijkt. Er komt geen kleine `"turn"` of `"curve"` meer bij. Die kleine afwijking telt mee in de volgende draai, zodat de missie toch klopt.
- **Rustiger rijden:** rijden gaat nu 80 mm/s (was 120), draaien 30 graden/s (was 45). Met SHIFT: 25 mm/s en 10 graden/s. De robot vertrekt en remt ook zachter.
- **Geen schommelen meer bij het vertrekken:** rij je rechtdoor, dan rijdt de robot eerst een kwart seconde heel traag. Zo trekken beide motoren de speling tussen de tandwielen weg voor hij versnelt. Ook stuurt de PID minder hard bij (`MAX_CORRECTIE` 10 in plaats van 20).
- Al deze getallen kan je zelf aanpassen bovenaan `vrij_rijden.py`.

**Welke bestanden?** `robot/vrij_rijden.py`, `computer/stuur_robot.py`, `robot/supportcode.py` (enkel `VERSIE`) en de uitleg.

---

## Versie 2026-10-14

Rijden met het toetsenbord kan nu op Windows **zonder iets te installeren**: dubbelklik op `stuur_robot.exe`.

**Wat moet je doen?**
- Download **[stuur_robot.exe](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/stuur_robot.exe)** en zet het in een eigen map (bijvoorbeeld `Documenten/robot`). Dubbelklik erop om te starten. Python en `pip install` heb je hiervoor niet meer nodig.
- Toont Windows *"Windows heeft uw pc beschermd"*? Klik op **Meer informatie** en dan **Toch uitvoeren**.
- Heet jullie hub niet `githo botic`? Maak dan in dezelfde map een bestand `hubnaam.txt` met daarin de naam van jullie hub.
- Werk je op een Mac? Gebruik dan zoals vroeger [stuur_robot.py](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/stuur_robot.py) met Python.
- **De code op de hub hoeft niet te veranderen.** Enkel het versienummer in `supportcode.py` is nieuw. Wil je dat toch bijwerken, gebruik dan [robot-zonder-missies.zip](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/robot-zonder-missies.zip) zoals altijd.
- **`missies.py` hoeft niet te veranderen.** Jullie missies blijven zoals ze zijn.

**Wat is er nieuw?**
- **stuur_robot.exe:** het programma voor de computer als Windows-app. GitHub maakt het automatisch bij elke nieuwe versie.
- Na het stoppen blijft het venster open tot je op ENTER drukt, zodat je de opname rustig kan lezen.
- **hubnaam.txt:** een andere naam voor de hub instellen zonder in de code te moeten werken.

**Welke bestanden?** `computer/stuur_robot.py`, `robot/supportcode.py` (enkel `VERSIE`), `.github/workflows/maak-downloads.yml` en de uitleg.

---

## Versie 2026-10-12b

Rijden met het toetsenbord is nu veel handiger om missies te maken: de robot neemt alles op.

**Wat moet je doen?**
- Maak eerst een back-up in Pybricks Code (**Backup all files**).
- Download [robot-zonder-missies.zip](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/robot-zonder-missies.zip) en importeer het in Pybricks Code. Kies telkens voor vervangen.
- Typ één keer in de terminal: `pip install rich` (een nieuw onderdeel voor het scherm van `stuur_robot.py`).
- Download ook de nieuwe [stuur_robot.py](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/stuur_robot.py) en zet ze in de plaats van de oude. De oude `stuur_robot.py` werkt **niet** met de nieuwe code op de hub (en omgekeerd). De computer waarschuwt je als het niet past.
- **`missies.py` hoeft niet te veranderen.** Jullie missies blijven zoals ze zijn.

**Wat is er nieuw?**
- **Opnemen:** elke beweging die je met het toetsenbord maakt, wordt automatisch een stap. Begin je aan een andere soort beweging (bijvoorbeeld van rijden naar draaien), dan wordt de vorige een stap. Alle stappen komen in `opname.txt` op de computer, klaar om in `missies.py` te plakken, met hun stapnummer erbij.
- **Letter V in het menu:** vrij rijden zit nu in `main.py`. Je hoeft dus geen ander programma meer op de hub te zetten, en ook niet te onthouden om `main.py` terug te zetten.
- **BACKSPACE** wist de laatste stap en de robot rijdt terug, zodat je opnieuw kan proberen.
- **Nieuw scherm op de computer:** `stuur_robot.py` toont nu een overzichtelijk scherm met vaste vakken: wat er gebeurt, de huidige stap, de instellingen, de opname, alle toetsen en de laatste meldingen. Geen tekst meer die voorbijschuift.
- **SPATIE** sluit de huidige stap af. (SPATIE zet niet meer zelf het nulpunt: dat is niet meer nodig.) **ENTER** toont de opname groot, over het hele scherm.
- **R** wist de opname en begint opnieuw.
- **P** speelt alles af op wedstrijdsnelheid, zoals in de echte missie. Zo zie je meteen of het ook snel goed gaat.
- **Verder vanaf een missie:** laat de robot in de testmodus een stuk van een missie rijden en druk daarna RECHTS (als het lampje groen is). Je rijdt dan verder met het toetsenbord vanaf de plek waar de missie eindigt. De nieuwe stappen krijgen meteen de juiste nummers, en `opname.txt` zegt waar je ze moet plakken.
- **Bochten:** Z en Q (of D) samen wordt een `("curve", straal, graden)`-stap.
- **Stapgrootte** in de stapmodus kies je met de toetsen 1, 2 en 3 (fijn, normaal, grof).
- De metingen van de huidige stap staan op één regel die zich steeds aanpast, in plaats van 10 nieuwe regels per seconde.
- De snelheid in opgenomen attachment-stappen stel je in bovenaan `vrij_rijden.py` (`ATTACHMENT_SNELHEID_IN_MISSIE`).
- In de stapmodus kan de knop op de hub nu ook tijdens een stap stoppen.

**Gewijzigde bestanden:** `robot/vrij_rijden.py`, `robot/main.py`, `robot/supportcode.py` (enkel `VERSIE`), `computer/stuur_robot.py`.

---

## Versie 2026-10-12

De eerste versie voor het seizoen BIOGLOW Founders Edition.

**Wat moet je doen?**
- Eerste keer: download [robot-volledig.zip](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/robot-volledig.zip) en importeer het in Pybricks Code.
- Had je al code van vorig seizoen op de computer? Maak eerst een back-up (**Backup all files**) en importeer dan de volledige ZIP. De oude missies passen toch niet meer bij de nieuwe mat.

**Wat is er nieuw?**
- De missies van vorig seizoen zijn verwijderd. Missies A tot E zijn leeg en klaar om in te schrijven.
- Bij het opstarten kijkt `main.py` alle missies na op tikfouten. Bij een fout wordt het lampje rood en zie je de letter en het stapnummer.
- Het menu maakt zijn lijst van letters zelf uit `missies.py`. Een nieuwe missie toevoegen doe je dus enkel nog in `missies.py`.
- Na een noodstop vertrekt de robot niet meer opnieuw als je de knop te lang vasthoudt.
- In `stuur_robot.py` zet SPATIE na het tonen meteen het nulpunt. Elke regel die je krijgt is dus precies één stap.
- De wielmotoren heten nu `LEFT_MOTOR` en `RIGHT_MOTOR`.
- `Stop.COAST` bij een `run_angle`-stap werkt nu echt (vroeger werd het genegeerd).
- `main.py` toont bij het opstarten het versienummer.

**Gewijzigde bestanden:** alle bestanden.
