# Wurmkompost Monitor

HACS Custom Integration für Home Assistant Core / Container / OS.

Diese Integration bewertet die Temperatur in deinem Wurmgefäß und kombiniert sie mit der Wettervorhersage, um frühzeitig vor Kälte und Hitze zu warnen.

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
- Vorwarnungen aus der **stündlichen Wettervorhersage**
- Optionen-Dialog zum Anpassen aller Temperaturgrenzen
- Eigene Sensoren und Binary Sensoren für Dashboard und Automationen

## Entitäten

### Sensoren

- `sensor.<name>_temperatur`
- `sensor.<name>_status`
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

1. Dieses Repository in GitHub anlegen.
2. In den Dateien `manifest.json` und `entity.py` die Platzhalter `USER` durch deinen GitHub-Namen / Repo-Link ersetzen.
3. In HACS `Benutzerdefiniertes Repository` hinzufügen.
4. Typ `Integration` wählen.
5. `Wurmkompost Monitor` installieren.
6. Home Assistant neu starten.
7. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Wurmkompost Monitor**.
8. Im Dialog Temperatur- und Wetter-Entity auswählen.

## Beispiel-Dashboard

```yaml
cards:
  - type: gauge
    entity: sensor.wurmkompost_temperatur
    min: -5
    max: 40
    name: Wurmtemperatur
    severity:
      red: 35
      yellow: 29
      green: 18
  - type: tile
    entity: sensor.wurmkompost_status
    name: Wurmstatus
  - type: tile
    entity: sensor.wurmkompost_wetterwarnung
    name: Vorwarnung
  - type: entities
    entities:
      - binary_sensor.wurmkompost_frostalarm
      - binary_sensor.wurmkompost_hitzealarm
      - binary_sensor.wurmkompost_kaeltewarnung
      - binary_sensor.wurmkompost_hitzewarnung
```

## Hinweise

- Die Integration nutzt `weather.get_forecasts` mit `hourly`, also die stündliche Wettervorhersage der gewählten `weather.*`-Entität.
- Alle eigenen Temperaturwerte werden intern als **°C** geführt.
- Wenn dein Temperatursensor in `°F` misst, wird er automatisch nach `°C` umgerechnet.

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
hacs.json
```
