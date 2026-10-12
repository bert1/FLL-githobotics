# Wijzigingen

Hier staat bij elke nieuwe versie wat er veranderd is, en wat jij moet doen om bij te werken.
De nieuwste versie staat altijd bovenaan.

Welke versie staat er op jullie robot? Start `main.py` in Pybricks Code. Onderaan verschijnt bijvoorbeeld `githobotics code versie 2026-10-12`.

Hoe werk je bij? Zie [1. GitHub en Pybricks](docs/1-github-en-pybricks.md#er-is-een-nieuwe-versie-bijwerken).

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
