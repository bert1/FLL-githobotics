# 4. Uitleg van de code

Hier staat per bestand wat het doet. Wil je een missie schrijven? Dan heb je vooral [3. Missies schrijven](3-missies-schrijven.md) nodig.

**Inhoud**
- [supportcode.py: de gereedschapskist](#supportcodepy-de-gereedschapskist)
- [main.py: het wedstrijdprogramma](#mainpy-het-wedstrijdprogramma)
- [vrij_rijden.py en stuur_robot.py: rijden met het toetsenbord](#vrij_rijdenpy-en-stuur_robotpy-rijden-met-het-toetsenbord)
- [Wat is PID?](#wat-is-pid)

## supportcode.py: de gereedschapskist

Dit bestand voer je nooit zelf uit. Andere bestanden halen er hun onderdelen uit met `import`.

**1. Robot setup.** Hier staat hoe de robot gebouwd is:

| Naam | Poort | Wat |
|---|---|---|
| `LEFT_MOTOR` | C | linker wiel |
| `RIGHT_MOTOR` | D | rechter wiel |
| `LEFT_ATTACHMENT` | E | linker motor voor een opzetstuk |
| `RIGHT_ATTACHMENT` | F | rechter motor voor een opzetstuk |

- `WHEEL_DIAMETER = 62.4`: de diameter van een wiel in mm. Klopt dit niet, dan rijdt de robot te ver of niet ver genoeg.
- `AXLE_TRACK = 153`: de afstand tussen de twee wielen in mm. Klopt dit niet, dan draait de robot te veel of te weinig.
- `DRIVE_BASE`: combineert de twee wielmotoren tot één "rijdend onderstel". Daarmee kan je zeggen "rij 300 mm" in plaats van elke motor apart te sturen.

**2. Veiligheidsfuncties.** `safe_straight`, `safe_turn`, `safe_curve`, `safe_wait` en `safe_run_angle` doen hetzelfde als de gewone Pybricks-functies, maar kijken elke 10 milliseconden of je op de middelste knop drukt. Zo ja, dan roept `check_stop()` een `MissionStop` op: alle motoren stoppen, het lampje wordt rood en de hub piept.

**3. Menu.** `next_program` en `prior_program` gaan één stap vooruit of achteruit in de lijst van missies. Het teken `%` zorgt dat je na de laatste letter terug bij de eerste uitkomt. `wacht_tot_losgelaten()` wacht tot je alle knoppen van de hub loslaat. Zonder die functie denkt het programma dat je opnieuw drukt zolang je de knop vasthoudt.

**4. Snelheidsprofielen.**
- `set_precieze_modus()`: rustig rijden, gyro aan. Dit is de normale modus.
- `set_snelle_modus()`: zo snel mogelijk, gyro uit. Enkel om op het einde terug naar de basis te rijden.
- `start_missie()`: zet afstand en richting op 0 op de plek waar de robot nu staat. Dit gebeurt automatisch bij elke missie.

**5. Stappen-systeem.** `voer_stappen_uit(stappen)` loopt door de lijst van stappen uit `missies.py` en voert ze één voor één uit. Het nummer van de stap verschijnt op het scherm. Met `start_bij` en `eind_stap` kan je maar een stukje uitvoeren (dat gebruikt de testmodus).

**5b. Missies controleren.** `controleer_stappen(stappen)` kijkt een missie na op tikfouten, nog voor de robot rijdt: bestaat de soort stap, staan er genoeg getallen, is een motor echt een motor, ... `main.py` doet dit bij het opstarten voor alle missies. In `STAP_SOORTEN` staat welke soorten stappen er zijn en hoeveel waarden erbij horen. Maak je een nieuwe soort stap in `voer_stappen_uit`, zet ze dan ook in `STAP_SOORTEN`.

**6. `safe_gyro_sprint`.** Een speciale functie om met volle kracht rechtdoor te rijden, met een eigen PID-regeling (zie [Wat is PID?](#wat-is-pid) onderaan). Voor gewone missies gebruik je gewoon `("straight", ...)`.

## main.py: het wedstrijdprogramma

Dit programma toont een letter op het scherm van de hub. De knoppen:

| Knop | Wat gebeurt er? | Kleur lampje |
|---|---|---|
| LINKS / RECHTS | vorige / volgende missie | blauw (**rood** als die missie een fout bevat) |
| MIDDEN | missie starten (pas als je loslaat) | oranje tijdens het rijden |
| MIDDEN tijdens het rijden | noodstop (laat de knop daarna los) | rood |
| LINKS + RECHTS samen | testmodus | |

Bij het opstarten worden eerst alle missies gecontroleerd op tikfouten (zie [Missies schrijven](3-missies-schrijven.md#tikfout-in-een-missie)).

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

## vrij_rijden.py en stuur_robot.py: rijden met het toetsenbord

Hiermee rijd je de robot met de hand naar de juiste plek, en lees je af hoeveel mm en graden dat was. Die getallen gebruik je dan in `missies.py`.

**Eenmalig klaarzetten op de computer:**
1. Installeer Python van [python.org](https://www.python.org/downloads/) (vink bij het installeren *Add Python to PATH* aan).
2. Download **[stuur_robot.py](https://github.com/bert1/FLL-githobotics/releases/download/nieuwste/stuur_robot.py)** en zet het in een eigen map, bijvoorbeeld `Documenten/robot`.
3. Open een terminal (Windows: zoek naar *Opdrachtprompt*) en typ:

```
pip install bleak pynput
```

Ga daarna in de terminal naar de map met `stuur_robot.py`, bijvoorbeeld met `cd Documenten/robot`.

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
| SPATIE | toon een kant-en-klare regel om in `missies.py` te plakken, en zet daarna meteen het nulpunt |
| ESC | stoppen |
| knop op de hub | stopt altijd meteen |

Alles wat de hub terugstuurt wordt ook bewaard in `rijlog.txt` op de computer.

**Werkwijze per stap:** rij rechtdoor, druk SPATIE, draai, druk SPATIE, ... Na elke SPATIE wordt het nulpunt automatisch gezet, dus elke regel die je krijgt is precies één stap. Je hoeft geen R meer te drukken. Bewegingen die 0 zijn worden niet getoond. Druk SPATIE best als de robot stilstaat: het nulpunt zetten stopt de robot even.

**Veiligheid:** komt er 0,5 seconde lang niets binnen van de computer (verbinding weg), dan stopt de robot vanzelf.

**Instellingen** staan bovenaan `vrij_rijden.py`: snelheden, stapgrootte en de PID-waarden. Met `GEBRUIK_EIGEN_PID = False` gebruik je de ingebouwde gyroregeling van Pybricks in plaats van onze eigen PID. Probeer beide en kies wat het rechtst rijdt.

Heet jullie hub anders dan `githo botic`? Pas dan `HUB_NAME` bovenaan `stuur_robot.py` aan.

**Na het uitzoeken: zet `main.py` terug op de hub voor de wedstrijd!**

---

## Wat is PID?

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

---

[Terug naar de startpagina](../README.md)
