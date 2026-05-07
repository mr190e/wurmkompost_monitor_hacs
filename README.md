# Wurmkompost Monitor

HACS Custom Integration für Home Assistant Core / Container / OS.

Diese Integration bewertet **Temperatur und Feuchtigkeit** in deinem Wurmgefäß und kombiniert die Werte mit der Wettervorhersage **inklusive Sonnen-Uplift**, um frühzeitig vor Kälte, Hitze, Vertrocknung und Staunässe zu warnen.

## Neu in Version 0.4.1

- Realistischere Default-Schwellen für Luftfeuchte-Sensoren in der Kiste (`air_in_bin`): Wohlfühlbereich jetzt 65–92 % statt 85–95 %, weil ein belüfteter Behälter über feuchtem Substrat normal bei 65–80 % RH liegt
- README-Erklärung zur Luftfeuchte als indirektem Indikator ergänzt

## Neu in Version 0.4.0

- **Standort-Dropdown** (Schatten, Halbschatten, volle Sonne) – bezieht Sonneneinstrahlung in die Hitze-Vorwarnung ein
- Sonnen-Uplift-Modell: Stundenprofil × Wolkenfaktor × Standort-Maximum, getrennt einstellbar für Halbschatten und volle Sonne
- **Feuchtigkeits-Sensortyp** wählbar (Substratfeuchte oder Luftfeuchte in der Kiste, z. B. SNZB-02WD); typgerechte Default-Schwellen werden bei der Einrichtung vorausgewählt
- Forecast-Sensor zeigt jetzt zusätzlich `ambient_c`, `sonnenzuschlag_c` und das Wetter zum prognostizierten Maximum

## Neu in Version 0.3.0

- **Optionaler Feuchtigkeitssensor** im Einrichtungsdialog (z. B. Substrat-/Boden­feuchte oder rel. Luftfeuchte)
- Eigene Statuszonen für Feuchtigkeit von `Vertrocknet` bis `Ertrunken`
- Zusätzliche Binary-Sensoren: `Vertrocknungsalarm`, `Ertrinkungsalarm`, `Trocken-` und `Nasswarnung`
- **Kombinierte Wurmstimmung**: Emoji und Botschaft spiegeln das schlimmste von Temperatur und Feuchtigkeit
- Neuer Mood `Doppelter Notfall` (🪱☠️) für gleichzeitige kritische Bedingungen
- Beispiel-Dashboard um Feuchtigkeits-Gauge und konditionale Alarmkarten erweitert

## Funktionen

- Dropdown im Einrichtungsdialog für **Temperatursensor**
- Dropdown im Einrichtungsdialog für **Feuchtigkeitssensor** (optional, akzeptiert `humidity` und `moisture`)
- Dropdown im Einrichtungsdialog für **Wetter-Entität**
- Statuszonen für die Temperatur:
  - `ALARM: Sie erfrieren`
  - `Zu kalt`
  - `Kühl`
  - `Wohlfühlbereich`
  - `Warm`
  - `Zu warm`
  - `ALARM: Hitzetod`
- Statuszonen für die Feuchtigkeit:
  - `ALARM: Sie vertrocknen`
  - `Zu trocken`
  - `Etwas trocken`
  - `Feuchtigkeit optimal`
  - `Etwas feucht`
  - `Zu nass`
  - `ALARM: Sie ertrinken`
- **Wurm-Stimmungsanzeige** mit Emojis wie `🪱🥶`, `🪱😄`, `🪱🥵`, `🪱🏜️`, `🪱🌊`, `🪱☠️`
- Vorwarnungen aus der **stündlichen Wettervorhersage**
- Optionen-Dialog zum Anpassen aller Temperatur- und Feuchtigkeitsgrenzen

## Entitäten

### Sensoren

- `sensor.<name>_temperatur`
- `sensor.<name>_feuchtigkeit` *(nur bei konfiguriertem Feuchtigkeitssensor)*
- `sensor.<name>_status`
- `sensor.<name>_feuchtigkeitsstatus` *(nur bei konfiguriertem Feuchtigkeitssensor)*
- `sensor.<name>_wurmstimmung`
- `sensor.<name>_wurmgesicht` *(standardmäßig deaktiviert, optional für Templates)*
- `sensor.<name>_wetterwarnung`
- `sensor.<name>_prognose_minimum`
- `sensor.<name>_prognose_maximum`

### Binary Sensoren

- `binary_sensor.<name>_frostalarm`
- `binary_sensor.<name>_hitzealarm`
- `binary_sensor.<name>_kaeltewarnung`
- `binary_sensor.<name>_hitzewarnung`
- `binary_sensor.<name>_vertrocknungsalarm` *(nur bei konfiguriertem Feuchtigkeitssensor)*
- `binary_sensor.<name>_ertrinkungsalarm` *(nur bei konfiguriertem Feuchtigkeitssensor)*
- `binary_sensor.<name>_trockenwarnung` *(nur bei konfiguriertem Feuchtigkeitssensor)*
- `binary_sensor.<name>_nasswarnung` *(nur bei konfiguriertem Feuchtigkeitssensor)*

## Standardgrenzen

### Temperatur

- Erfrierungsalarm: `<= 0 °C`
- Zu kalt: `< 10 °C`
- Kühl: `10–17.9 °C`
- Wohlfühlbereich: `18–25 °C`
- Warm: `25.1–29 °C`
- Zu warm: `29.1–35 °C`
- Hitzetod: `> 35 °C`

### Feuchtigkeit

Die Defaults werden anhand des **Sensor-Typs** gesetzt, den du beim Einrichten wählst.

**Substratfeuchte (Bodenfeuchtesensor, % Volumenwassergehalt)**:

- Vertrocknungsalarm: `<= 40 %`
- Zu trocken: `< 60 %`
- Etwas trocken: `60–69.9 %`
- Optimal: `70–85 %`
- Etwas feucht: `85.1–90 %`
- Zu nass: `90.1–94.9 %`
- Ertrinkungsalarm: `>= 95 %`

**Luftfeuchte in der Kiste (z. B. SNZB-02WD, % rel. Luftfeuchte)**:

Sensoren, die im/auf dem Substrat liegen, messen die direkt darüberliegende Luftfeuchte. Diese ist nur ein **indirekter Indikator** für den Zustand des Substrats und schwankt stark mit Belüftung und Deckelbauweise; die Wohlfühl-Bandbreite ist daher absichtlich weit gefasst, damit ein gut belüfteter Behälter mit 65–80 % RH nicht ständig „Zu trocken" meldet.

- Vertrocknungsalarm: `<= 40 %`
- Zu trocken: `< 55 %`
- Etwas trocken: `55–64.9 %`
- Optimal: `65–92 %`
- Etwas feucht: `92.1–97 %`
- Zu nass: `97.1–98.9 %`
- Ertrinkungsalarm: `>= 99 %`

### Sonnen-Uplift (Mittagshitze)

Die Wettervorhersage liefert die Lufttemperatur im Schatten. Eine Wurmkiste in der Sonne kann mittags deutlich heißer werden – die Integration rechnet das vorab in die Hitzewarnung ein:

```
Sonnen-Zuschlag = Standort-Max × Stundenprofil × Wolkenfaktor
```

- Standort-Max: Schatten = 0 °C, Halbschatten = 5 °C (Default), volle Sonne = 12 °C (Default)
- Stundenprofil: 0 vor 8 / nach 19 Uhr, Peak 12–14 Uhr (lokale Zeit)
- Wolkenfaktor aus dem `condition`-Feld der Vorhersage (sunny=1.0, partlycloudy=0.6, cloudy=0.3, rainy=0.1 …)

Beispiel: Halbschatten, sunny, 13 Uhr, 28 °C Lufttemperatur → 28 + 5 × 1.0 × 1.0 = **33 °C** für die Klassifikation. Das löst frühzeitig die Hitzewarnung aus.

Die Maximalwerte für Halbschatten und volle Sonne sind in den Optionen einstellbar.

## Installation über HACS

1. Dieses Repository in GitHub anlegen oder aktualisieren.
2. In HACS `Benutzerdefiniertes Repository` hinzufügen.
3. Typ `Integration` wählen.
4. `Wurmkompost Monitor` installieren.
5. Home Assistant neu starten.
6. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Wurmkompost Monitor**.
7. Im Dialog Temperatur-, optional Feuchtigkeits-, Wetter-Entity sowie **Sensor-Typ** und **Standort** auswählen.

Wer den Feuchtigkeitssensor erst später nachrüstet, kann ihn in den **Optionen** der Integration ergänzen – die zusätzlichen Entitäten erscheinen automatisch nach dem Reload.

## Lovelace-Beispiel

Eine fertige Vorlage findest du in `examples/lovelace_wurmkompost.yaml`.

Die Vorlage zeigt:

- oben eine **Gauge** für die Temperatur
- darunter eine **Gauge** für die Feuchtigkeit
- eine **große Wurmkarte** mit Emoji, Stimmung und Botschaft
- darunter nur die wirklich wichtigen Informationen
- Warn- und Alarmkarten **nur dann, wenn sie aktiv sind** (auch für Vertrocknung/Staunässe)

## Hinweise

- Die Integration nutzt `weather.get_forecasts` mit `hourly`, also die stündliche Wettervorhersage der gewählten `weather.*`-Entität.
- Alle eigenen Temperaturwerte werden intern als **°C** geführt.
- Wenn dein Temperatursensor in `°F` misst, wird er automatisch nach `°C` umgerechnet.
- Feuchtigkeit wird in **%** geführt. Liefert dein Sensor einen Wert zwischen `0` und `1`, wird er automatisch auf 0–100 % skaliert.
- Geeignet sind Sensoren mit `device_class: humidity` (Luftfeuchte) **oder** `device_class: moisture` (Substratfeuchte) bzw. einer Einheit `%`.
- Die grafische Darstellung entsteht in Lovelace; die Integration liefert dafür die zusätzlichen Entitäten und Attribute.
- Wenn du `sensor.<name>_wurmgesicht` im Dashboard direkt verwenden willst, kannst du die Entität in der Registry wieder aktivieren.

## Repository-Struktur

```text
custom_components/wurmkompost/
  __init__.py
  binary_sensor.py
  config_flow.py
  const.py
  coordinator.py
  entity.py
  manifest.json
  sensor.py
  strings.json
  translations/
    de.json
    en.json
examples/
  lovelace_wurmkompost.yaml
hacs.json
```
