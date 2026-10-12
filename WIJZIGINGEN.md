# Wijzigingen

Hier staat bij elke nieuwe versie wat er veranderd is, en wat jij moet doen om bij te werken.
De nieuwste versie staat altijd bovenaan.

Welke versie staat er op jullie robot? Start `main.py` in Pybricks Code. Onderaan verschijnt bijvoorbeeld `githobotics code versie 2026-10-12`.

Hoe werk je bij? Zie [1. GitHub en Pybricks](docs/1-github-en-pybricks.md#er-is-een-nieuwe-versie-bijwerken).

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
