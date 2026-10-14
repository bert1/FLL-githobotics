# 1. GitHub en Pybricks

Nog nooit met GitHub gewerkt? Geen probleem. Je hebt geen account nodig om de code te downloaden.

**Inhoud**
- [Wat is GitHub?](#wat-is-github)
- [Wat is Pybricks Code?](#wat-is-pybricks-code)
- [De eerste keer: alles op de robot zetten](#de-eerste-keer-alles-op-de-robot-zetten)
- [Er is een nieuwe versie: bijwerken](#er-is-een-nieuwe-versie-bijwerken)
- [Eén bestand downloaden](#één-bestand-downloaden)
- [Een back-up maken in Pybricks Code](#een-back-up-maken-in-pybricks-code)
- [Een oudere versie bekijken](#een-oudere-versie-bekijken)
- [Woorden die je op GitHub tegenkomt](#woorden-die-je-op-github-tegenkomt)

## Wat is GitHub?

GitHub is een website waar programmeurs hun code bewaren. Je kan het vergelijken met een gedeelde map in de cloud, maar met een extra: GitHub onthoudt **elke versie** van elk bestand. Zo kan je altijd zien wat er veranderd is, en wie het veranderd heeft.

Onze code staat in een **repository** (kort: repo). Dat is gewoon een projectmap. Die van ons heet `FLL-githobotics` en ziet er zo uit:

```
FLL-githobotics/
├── README.md              ← de startpagina (die zie je onder de lijst met bestanden)
├── WIJZIGINGEN.md         ← wat er in elke nieuwe versie veranderd is
├── robot/                 ← DEZE bestanden gaan naar Pybricks Code
│   ├── main.py
│   ├── missies.py
│   ├── supportcode.py
│   └── vrij_rijden.py
├── computer/              ← dit draait op de computer, NIET op de robot
│   └── stuur_robot.py
└── docs/                  ← alle uitleg, zoals deze pagina
```

Klik op een map om erin te gaan, en op een bestand om het te lezen. Bovenaan zie je waar je bent, bijvoorbeeld `FLL-githobotics / robot / main.py`. Klik op `FLL-githobotics` om terug te gaan naar het begin.

## Wat is Pybricks Code?

Pybricks Code is de website waarmee we de LEGO hub programmeren: [code.pybricks.com](https://code.pybricks.com). Gebruik **Google Chrome** of **Microsoft Edge**, want andere browsers kunnen geen Bluetooth-verbinding maken met de hub.

Links in Pybricks Code staat een lijst met bestanden. Bovenaan die lijst staan drie knoppen. Wijs ze aan met de muis om hun naam te zien:

| Knop (Engels) | Wat doet hij? |
|---|---|
| **Create a new file** | een nieuw, leeg bestand maken |
| **Import a file** | bestanden van je computer toevoegen (ook een ZIP-bestand) |
| **Backup all files** | al je bestanden in één ZIP-bestand downloaden, als back-up |

**Belangrijk:** Pybricks Code bewaart je bestanden **in de browser** van de computer waarop je werkt. Op een andere computer zie je ze niet. Wis je de browsergegevens, dan zijn ze weg. Maak dus geregeld een [back-up](#een-back-up-maken-in-pybricks-code).

## De eerste keer: alles op de robot zetten

1. **Download** het bestand **[robot-volledig.zip](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/robot-volledig.zip)**. Daarin zitten de 4 bestanden voor de robot.
2. Open [code.pybricks.com](https://code.pybricks.com).
3. Klik links op **Import a file** en kies het ZIP-bestand dat je net gedownload hebt (meestal in de map *Downloads*). Je hoeft het niet eerst uit te pakken.
4. Je ziet nu links `main.py`, `missies.py`, `supportcode.py` en `vrij_rijden.py`.
5. Verbind met de hub (Bluetooth-knop bovenaan), open `main.py` en druk op de startknop (driehoekje).

Bij het opstarten print `main.py` in het venster onderaan welke versie van de code je hebt, bijvoorbeeld `githobotics code versie 2026-10-12`.

## Er is een nieuwe versie: bijwerken

De coach laat weten als er een nieuwe versie is. Wat er veranderd is, lees je in [WIJZIGINGEN.md](../WIJZIGINGEN.md).

> **Let op: overschrijf je eigen missies niet!** In `missies.py` staan de missies die jullie zelf geschreven hebben. Daarom is er een aparte ZIP **zonder** `missies.py`.

1. **Maak eerst een back-up** van wat je nu hebt (zie [hieronder](#een-back-up-maken-in-pybricks-code)). Dan kan je altijd terug.
2. **Download** het bestand **[robot-zonder-missies.zip](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/robot-zonder-missies.zip)**.
3. Klik in Pybricks Code op **Import a file** en kies dat ZIP-bestand.
4. Pybricks Code ziet dat er al bestanden met dezelfde naam zijn en **vraagt of je ze wil vervangen**. Kies telkens voor vervangen.
5. Open `main.py`, start het programma en kijk onderaan of het nieuwe versienummer verschijnt.

Staat er in WIJZIGINGEN.md dat er ook iets in `missies.py` veranderd is? Dan staat daar ook precies wat je zelf moet aanpassen in jullie `missies.py`. Neem dan **niet** de volledige ZIP, want dan ben je je missies kwijt.

## Eén bestand downloaden

Moet je maar één bestand hebben (bijvoorbeeld `computer/stuur_robot.py`)?

1. Klik op GitHub op het bestand.
2. Rechtsboven het bestand staat een knop met een **pijltje naar beneden** (*Download raw file*). Klik erop.
3. Het bestand staat nu in je map *Downloads*. Voor de robot importeer je het in Pybricks Code met **Import a file**.

Of download ook dit rechtstreeks: **[stuur_robot.exe](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/stuur_robot.exe)** (Windows, niets te installeren) of **[stuur_robot.py](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/stuur_robot.py)** (Mac, met Python).

## Een back-up maken in Pybricks Code

1. Klik links in Pybricks Code op **Backup all files**.
2. Er wordt een ZIP-bestand gedownload met al je bestanden.
3. Zet dat bestand op een veilige plek, bijvoorbeeld in de gedeelde map van het team. Geef het een duidelijke naam, zoals `backup-2026-10-12.zip`.

Terugzetten doe je met **Import a file**: kies dat ZIP-bestand.

## Een oudere versie bekijken

GitHub bewaart elke versie.

1. Ga naar een bestand, bijvoorbeeld `robot/missies.py`.
2. Klik rechtsboven op **History** (een klokje).
3. Je ziet een lijst van alle wijzigingen, de nieuwste bovenaan. Klik op een wijziging om te zien wat er veranderd is: **rood** is weggehaald, **groen** is toegevoegd.
4. Wil je het hele bestand van toen zien? Klik bij die wijziging op de knop **<>** (*Browse repository at this point*).

## Woorden die je op GitHub tegenkomt

| Woord | Betekenis |
|---|---|
| repository (repo) | de projectmap met al onze code |
| commit | één opgeslagen wijziging, met een korte uitleg erbij |
| branch | een aparte versie om iets nieuws uit te proberen. De echte versie heet **main** |
| release | een pakketje om te downloaden. Ons pakketje heet **nieuwste** |
| README | de uitlegpagina die GitHub automatisch toont |
| `.md` | een tekstbestand met opmaak (Markdown), GitHub toont het als een mooie pagina |
| raw | het bestand zonder opmaak, zoals het echt is |

---

[Terug naar de startpagina](../README.md)
