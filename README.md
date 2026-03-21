# Wurmkompost Monitor

HACS Custom Integration für Home Assistant Core / Container / OS.

Diese Integration bewertet die Temperatur in deinem Wurmgefäß und kombiniert sie mit der Wettervorhersage, um frühzeitig vor Kälte und Hitze zu warnen.

## Neu in Version 0.2.0

- **Wurmstimmung** als eigene Entität
- **Wurmgesicht** als Emoji-Entität für eine spielerische Anzeige
- zusätzliche Attribute für **Farbe**, **Emoji** und **Wurm-Botschaft**
- Lovelace-Beispiel für eine deutlich **grafischere Darstellung** mit Gauge, Status und Emoji

## Funktionen

- Dropdown im Einrichtungsdialog für **Temperatursensor**
- Dropdown im Einrichtungsdialog für **Wetter-Entität**
- Statuszonen für Kompostwürmer:
  - `ALARM: Sie erfrieren`
  - `Zu kalt`
  - `Kühl`
  - `Wohlfühlbereich`
  - `Warm`
  - `Zu warm`
  - `ALARM: Hitzetod`
- **Wurm-Stimmungsanzeige** mit Emojis wie `🪱🥶`, `🪱😄`, `🪱🥵`
- Vorwarnungen aus der **stündlichen Wettervorhersage**
- Optionen-Dialog zum Anpassen aller Temperaturgrenzen
- Eigene Sensoren und Binary Sensoren für Dashboard und Automationen

## Entitäten

### Sensoren

- `sensor.<name>_temperatur`
- `sensor.<name>_status`
- `sensor.<name>_wurmstimmung`
- `sensor.<name>_wurmgesicht`
- `sensor.<name>_wetterwarnung`
- `sensor.<name>_prognose_minimum`
- `sensor.<name>_prognose_maximum`

### Binary Sensoren

- `binary_sensor.<name>_frostalarm`
- `binary_sensor.<name>_hitzealarm`
- `binary_sensor.<name>_kaeltewarnung`
- `binary_sensor.<name>_hitzewarnung`

## Standardgrenzen

- Erfrierungsalarm: `<= 0 °C`
- Zu kalt: `< 10 °C`
- Kühl: `10–17.9 °C`
- Wohlfühlbereich: `18–25 °C`
- Warm: `25.1–29 °C`
- Zu warm: `29.1–35 °C`
- Hitzetod: `> 35 °C`

## Installation über HACS

1. Dieses Repository in GitHub anlegen oder aktualisieren.
2. In HACS `Benutzerdefiniertes Repository` hinzufügen.
3. Typ `Integration` wählen.
4. `Wurmkompost Monitor` installieren.
5. Home Assistant neu starten.
6. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Wurmkompost Monitor**.
7. Im Dialog Temperatur- und Wetter-Entity auswählen.

## Lovelace-Beispiel

Eine fertige Vorlage findest du in `examples/lovelace_wurmkompost.yaml`.

Die Vorlage nutzt nur Standard-Karten und zeigt:

- oben eine **Gauge** für die Temperatur
- darunter eine **große Emoji-/Stimmungsanzeige**
- darunter Status, Wetterwarnung und Alarme als Grid

## Hinweise

- Die Integration nutzt `weather.get_forecasts` mit `hourly`, also die stündliche Wettervorhersage der gewählten `weather.*`-Entität.
- Alle eigenen Temperaturwerte werden intern als **°C** geführt.
- Wenn dein Temperatursensor in `°F` misst, wird er automatisch nach `°C` umgerechnet.
- Die grafische Darstellung entsteht in Lovelace; die Integration liefert dafür die zusätzlichen Entitäten und Attribute.

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
