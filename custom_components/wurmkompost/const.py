from __future__ import annotations

from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "wurmkompost"
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

CONF_COMPOST_NAME = "compost_name"
CONF_TEMPERATURE_SENSOR = "temperature_sensor"
CONF_HUMIDITY_SENSOR = "humidity_sensor"
CONF_WEATHER_ENTITY = "weather_entity"
CONF_FREEZE_TEMP = "freeze_temp"
CONF_COLD_TEMP = "cold_temp"
CONF_COMFORT_MIN_TEMP = "comfort_min_temp"
CONF_COMFORT_MAX_TEMP = "comfort_max_temp"
CONF_WARM_TEMP = "warm_temp"
CONF_FATAL_HEAT_TEMP = "fatal_heat_temp"
CONF_FORECAST_HOURS = "forecast_hours"
CONF_COLD_WARNING_BUFFER = "cold_warning_buffer"
CONF_HEAT_WARNING_TEMP = "heat_warning_temp"

CONF_HUMIDITY_FATAL_DRY = "humidity_fatal_dry"
CONF_HUMIDITY_DRY = "humidity_dry"
CONF_HUMIDITY_COMFORT_MIN = "humidity_comfort_min"
CONF_HUMIDITY_COMFORT_MAX = "humidity_comfort_max"
CONF_HUMIDITY_WET = "humidity_wet"
CONF_HUMIDITY_FATAL_WET = "humidity_fatal_wet"
CONF_HUMIDITY_SENSOR_TYPE = "humidity_sensor_type"

CONF_SUN_EXPOSURE = "sun_exposure"
CONF_SUN_UPLIFT_FULL_SUN = "sun_uplift_full_sun"
CONF_SUN_UPLIFT_PARTIAL_SHADE = "sun_uplift_partial_shade"

HUMIDITY_TYPE_SUBSTRATE = "substrate"
HUMIDITY_TYPE_AIR_IN_BIN = "air_in_bin"

HUMIDITY_TYPE_LABELS: dict[str, str] = {
    HUMIDITY_TYPE_SUBSTRATE: "Substratfeuchte (Bodenfeuchtesensor)",
    HUMIDITY_TYPE_AIR_IN_BIN: "Luftfeuchte in der Kiste (z. B. SNZB-02WD)",
}

SUN_EXPOSURE_SHADE = "shade"
SUN_EXPOSURE_PARTIAL_SHADE = "partial_shade"
SUN_EXPOSURE_FULL_SUN = "full_sun"

SUN_EXPOSURE_LABELS: dict[str, str] = {
    SUN_EXPOSURE_SHADE: "Schatten",
    SUN_EXPOSURE_PARTIAL_SHADE: "Halbschatten",
    SUN_EXPOSURE_FULL_SUN: "Volle Sonne",
}

DEFAULT_COMPOST_NAME = "Wurmkompost"
DEFAULT_FREEZE_TEMP = 0.0
DEFAULT_COLD_TEMP = 10.0
DEFAULT_COMFORT_MIN_TEMP = 18.0
DEFAULT_COMFORT_MAX_TEMP = 25.0
DEFAULT_WARM_TEMP = 29.0
DEFAULT_FATAL_HEAT_TEMP = 35.0
DEFAULT_FORECAST_HOURS = 12
DEFAULT_COLD_WARNING_BUFFER = 2.0
DEFAULT_HEAT_WARNING_TEMP = 30.0

DEFAULT_HUMIDITY_FATAL_DRY = 40.0
DEFAULT_HUMIDITY_DRY = 60.0
DEFAULT_HUMIDITY_COMFORT_MIN = 70.0
DEFAULT_HUMIDITY_COMFORT_MAX = 85.0
DEFAULT_HUMIDITY_WET = 90.0
DEFAULT_HUMIDITY_FATAL_WET = 95.0

DEFAULT_HUMIDITY_SENSOR_TYPE = HUMIDITY_TYPE_SUBSTRATE
DEFAULT_SUN_EXPOSURE = SUN_EXPOSURE_PARTIAL_SHADE
DEFAULT_SUN_UPLIFT_FULL_SUN = 12.0
DEFAULT_SUN_UPLIFT_PARTIAL_SHADE = 5.0

# Type-specific default thresholds. Substrate moisture and in-bin air humidity
# behave very differently; with a moist substrate the air RH directly above it
# typically sits at 85-95 %, so an air sensor needs higher comfort bounds.
HUMIDITY_DEFAULTS_BY_TYPE: dict[str, dict[str, float]] = {
    HUMIDITY_TYPE_SUBSTRATE: {
        CONF_HUMIDITY_FATAL_DRY: 40.0,
        CONF_HUMIDITY_DRY: 60.0,
        CONF_HUMIDITY_COMFORT_MIN: 70.0,
        CONF_HUMIDITY_COMFORT_MAX: 85.0,
        CONF_HUMIDITY_WET: 90.0,
        CONF_HUMIDITY_FATAL_WET: 95.0,
    },
    HUMIDITY_TYPE_AIR_IN_BIN: {
        CONF_HUMIDITY_FATAL_DRY: 60.0,
        CONF_HUMIDITY_DRY: 75.0,
        CONF_HUMIDITY_COMFORT_MIN: 85.0,
        CONF_HUMIDITY_COMFORT_MAX: 95.0,
        CONF_HUMIDITY_WET: 97.0,
        CONF_HUMIDITY_FATAL_WET: 99.0,
    },
}

# Stundenprofil 0..1 für die Sonnen-Intensität (lokale Zeit). Vor 8 und ab 19
# Uhr null, Peak 12-14 Uhr.
SUN_HOUR_FACTORS: dict[int, float] = {
    8: 0.3, 9: 0.3,
    10: 0.7, 11: 0.7,
    12: 1.0, 13: 1.0, 14: 1.0,
    15: 0.7, 16: 0.7,
    17: 0.4, 18: 0.4,
}

# Wolken-/Wetterfaktor — wie viel der Sonneneinstrahlung durchkommt.
CONDITION_SUN_FACTOR: dict[str, float] = {
    "sunny": 1.0,
    "clear-night": 0.0,
    "partlycloudy": 0.6,
    "cloudy": 0.3,
    "fog": 0.1,
    "rainy": 0.1,
    "pouring": 0.0,
    "snowy": 0.0,
    "snowy-rainy": 0.0,
    "hail": 0.0,
    "windy": 0.7,
    "windy-variant": 0.7,
    "lightning": 0.3,
    "lightning-rainy": 0.2,
    "exceptional": 0.5,
}
DEFAULT_CONDITION_SUN_FACTOR = 0.5

DEFAULT_UPDATE_INTERVAL = timedelta(minutes=15)

STATUS_FREEZE = "alarm_erfrieren"
STATUS_COLD = "zu_kalt"
STATUS_COOL = "kuehl"
STATUS_COMFORT = "wohlfuehlbereich"
STATUS_WARM = "warm"
STATUS_HOT = "zu_warm"
STATUS_HEAT_DEATH = "alarm_hitzetod"
STATUS_UNKNOWN = "unbekannt"

HUMIDITY_FATAL_DRY = "alarm_vertrocknet"
HUMIDITY_DRY = "zu_trocken"
HUMIDITY_LOW = "leicht_trocken"
HUMIDITY_COMFORT = "feuchtigkeit_optimal"
HUMIDITY_HIGH = "leicht_feucht"
HUMIDITY_WET = "zu_nass"
HUMIDITY_FATAL_WET = "alarm_ertrunken"
HUMIDITY_UNKNOWN = "feuchtigkeit_unbekannt"
HUMIDITY_NOT_CONFIGURED = "feuchtigkeit_nicht_konfiguriert"

FORECAST_NONE = "keine_warnung"
FORECAST_COLD = "kaeltewarnung"
FORECAST_FREEZE = "frostwarnung"
FORECAST_HEAT = "hitzewarnung"
FORECAST_HEAT_DEATH = "extreme_hitzewarnung"

MOOD_FREEZE = "erfrierend"
MOOD_COLD = "frierend"
MOOD_COOL = "froestelnd"
MOOD_COMFORT = "zufrieden"
MOOD_WARM = "leicht_warm"
MOOD_HOT = "schwitzend"
MOOD_HEAT_DEATH = "notfall"
MOOD_UNKNOWN = "unklar"
MOOD_FATAL_DRY = "vertrocknend"
MOOD_DRY = "durstig"
MOOD_LOW_HUMIDITY = "leicht_durstig"
MOOD_HIGH_HUMIDITY = "feucht"
MOOD_WET = "zu_nass"
MOOD_FATAL_WET = "ertrinkend"
MOOD_DOUBLE_CRISIS = "doppelter_notfall"

STATUS_ORDER = [
    STATUS_FREEZE,
    STATUS_COLD,
    STATUS_COOL,
    STATUS_COMFORT,
    STATUS_WARM,
    STATUS_HOT,
    STATUS_HEAT_DEATH,
    STATUS_UNKNOWN,
]

HUMIDITY_ORDER = [
    HUMIDITY_FATAL_DRY,
    HUMIDITY_DRY,
    HUMIDITY_LOW,
    HUMIDITY_COMFORT,
    HUMIDITY_HIGH,
    HUMIDITY_WET,
    HUMIDITY_FATAL_WET,
    HUMIDITY_UNKNOWN,
    HUMIDITY_NOT_CONFIGURED,
]

FORECAST_ORDER = [
    FORECAST_NONE,
    FORECAST_COLD,
    FORECAST_FREEZE,
    FORECAST_HEAT,
    FORECAST_HEAT_DEATH,
]

STATUS_LABELS: dict[str, str] = {
    STATUS_FREEZE: "ALARM: Sie erfrieren",
    STATUS_COLD: "Zu kalt",
    STATUS_COOL: "Kühl",
    STATUS_COMFORT: "Wohlfühlbereich",
    STATUS_WARM: "Warm",
    STATUS_HOT: "Zu warm",
    STATUS_HEAT_DEATH: "ALARM: Hitzetod",
    STATUS_UNKNOWN: "Unbekannt",
}

HUMIDITY_LABELS: dict[str, str] = {
    HUMIDITY_FATAL_DRY: "ALARM: Sie vertrocknen",
    HUMIDITY_DRY: "Zu trocken",
    HUMIDITY_LOW: "Etwas trocken",
    HUMIDITY_COMFORT: "Feuchtigkeit optimal",
    HUMIDITY_HIGH: "Etwas feucht",
    HUMIDITY_WET: "Zu nass",
    HUMIDITY_FATAL_WET: "ALARM: Sie ertrinken",
    HUMIDITY_UNKNOWN: "Feuchtigkeit unbekannt",
    HUMIDITY_NOT_CONFIGURED: "Kein Feuchtigkeitssensor",
}

STATUS_ICONS: dict[str, str] = {
    STATUS_FREEZE: "mdi:snowflake-alert",
    STATUS_COLD: "mdi:snowflake-thermometer",
    STATUS_COOL: "mdi:thermometer-low",
    STATUS_COMFORT: "mdi:leaf-circle",
    STATUS_WARM: "mdi:thermometer",
    STATUS_HOT: "mdi:thermometer-high",
    STATUS_HEAT_DEATH: "mdi:fire-alert",
    STATUS_UNKNOWN: "mdi:help-circle-outline",
}

HUMIDITY_ICONS: dict[str, str] = {
    HUMIDITY_FATAL_DRY: "mdi:water-off",
    HUMIDITY_DRY: "mdi:water-alert",
    HUMIDITY_LOW: "mdi:water-minus",
    HUMIDITY_COMFORT: "mdi:water-check",
    HUMIDITY_HIGH: "mdi:water-plus",
    HUMIDITY_WET: "mdi:water-alert",
    HUMIDITY_FATAL_WET: "mdi:water-alert-outline",
    HUMIDITY_UNKNOWN: "mdi:help-circle-outline",
    HUMIDITY_NOT_CONFIGURED: "mdi:water-remove-outline",
}

STATUS_RECOMMENDATIONS: dict[str, str] = {
    STATUS_FREEZE: "Sofort isolieren oder an einen frostfreien Ort bringen.",
    STATUS_COLD: "Mehr Isolierung oder wärmeren Standort prüfen.",
    STATUS_COOL: "Okay, aber noch nicht optimal für aktive Kompostwürmer.",
    STATUS_COMFORT: "Alles gut: Das ist der Wohlfühlbereich der Würmer.",
    STATUS_WARM: "Beobachten, ausreichend Feuchte und Belüftung sicherstellen.",
    STATUS_HOT: "Kühlen, beschatten und Hitzestau vermeiden.",
    STATUS_HEAT_DEATH: "Sofort handeln: Kühlen und Hitzestau beenden.",
    STATUS_UNKNOWN: "Temperatursensor prüfen.",
}

HUMIDITY_RECOMMENDATIONS: dict[str, str] = {
    HUMIDITY_FATAL_DRY: "Notfall: Substrat sofort gründlich befeuchten und mit feuchtem Material abdecken.",
    HUMIDITY_DRY: "Mit Sprühflasche oder feuchtem Zeitungspapier nachfeuchten.",
    HUMIDITY_LOW: "Etwas Wasser ergänzen und Verdunstung beobachten.",
    HUMIDITY_COMFORT: "Feuchtigkeit ist im Idealbereich.",
    HUMIDITY_HIGH: "Trockenes Material (Karton, Zeitung, Laub) untermischen.",
    HUMIDITY_WET: "Belüftung verbessern und trockenes Strukturmaterial ergänzen, sonst wird es anaerob.",
    HUMIDITY_FATAL_WET: "Sofort: Wasser ablaufen lassen und reichlich trockenes Material einarbeiten.",
    HUMIDITY_UNKNOWN: "Feuchtigkeitssensor prüfen.",
    HUMIDITY_NOT_CONFIGURED: "Kein Feuchtigkeitssensor konfiguriert. In den Optionen nachrüsten.",
}

STATUS_COLORS: dict[str, str] = {
    STATUS_FREEZE: "#1e88e5",
    STATUS_COLD: "#42a5f5",
    STATUS_COOL: "#ffd54f",
    STATUS_COMFORT: "#43a047",
    STATUS_WARM: "#ffb300",
    STATUS_HOT: "#fb8c00",
    STATUS_HEAT_DEATH: "#e53935",
    STATUS_UNKNOWN: "#9e9e9e",
}

HUMIDITY_COLORS: dict[str, str] = {
    HUMIDITY_FATAL_DRY: "#bf360c",
    HUMIDITY_DRY: "#e64a19",
    HUMIDITY_LOW: "#ffb74d",
    HUMIDITY_COMFORT: "#43a047",
    HUMIDITY_HIGH: "#26a69a",
    HUMIDITY_WET: "#0288d1",
    HUMIDITY_FATAL_WET: "#01579b",
    HUMIDITY_UNKNOWN: "#9e9e9e",
    HUMIDITY_NOT_CONFIGURED: "#bdbdbd",
}

# Severity scale for combining temperature and humidity moods.
#  0 = optimal, 1 = leichte Abweichung, 2 = deutlich problematisch, 3 = lebensbedrohlich
TEMP_SEVERITY: dict[str, int] = {
    STATUS_COMFORT: 0,
    STATUS_COOL: 1,
    STATUS_WARM: 1,
    STATUS_COLD: 2,
    STATUS_HOT: 2,
    STATUS_FREEZE: 3,
    STATUS_HEAT_DEATH: 3,
    STATUS_UNKNOWN: 0,
}

HUMIDITY_SEVERITY: dict[str, int] = {
    HUMIDITY_COMFORT: 0,
    HUMIDITY_LOW: 1,
    HUMIDITY_HIGH: 1,
    HUMIDITY_DRY: 2,
    HUMIDITY_WET: 2,
    HUMIDITY_FATAL_DRY: 3,
    HUMIDITY_FATAL_WET: 3,
    HUMIDITY_UNKNOWN: 0,
    HUMIDITY_NOT_CONFIGURED: 0,
}

MOOD_BY_STATUS: dict[str, str] = {
    STATUS_FREEZE: MOOD_FREEZE,
    STATUS_COLD: MOOD_COLD,
    STATUS_COOL: MOOD_COOL,
    STATUS_COMFORT: MOOD_COMFORT,
    STATUS_WARM: MOOD_WARM,
    STATUS_HOT: MOOD_HOT,
    STATUS_HEAT_DEATH: MOOD_HEAT_DEATH,
    STATUS_UNKNOWN: MOOD_UNKNOWN,
}

MOOD_BY_HUMIDITY: dict[str, str] = {
    HUMIDITY_FATAL_DRY: MOOD_FATAL_DRY,
    HUMIDITY_DRY: MOOD_DRY,
    HUMIDITY_LOW: MOOD_LOW_HUMIDITY,
    HUMIDITY_COMFORT: MOOD_COMFORT,
    HUMIDITY_HIGH: MOOD_HIGH_HUMIDITY,
    HUMIDITY_WET: MOOD_WET,
    HUMIDITY_FATAL_WET: MOOD_FATAL_WET,
    HUMIDITY_UNKNOWN: MOOD_UNKNOWN,
    HUMIDITY_NOT_CONFIGURED: MOOD_COMFORT,
}

MOOD_LABELS: dict[str, str] = {
    MOOD_FREEZE: "Erfrierend",
    MOOD_COLD: "Frierend",
    MOOD_COOL: "Fröstelnd",
    MOOD_COMFORT: "Zufrieden",
    MOOD_WARM: "Leicht warm",
    MOOD_HOT: "Schwitzend",
    MOOD_HEAT_DEATH: "Notfall",
    MOOD_UNKNOWN: "Unklar",
    MOOD_FATAL_DRY: "Vertrocknend",
    MOOD_DRY: "Durstig",
    MOOD_LOW_HUMIDITY: "Leicht durstig",
    MOOD_HIGH_HUMIDITY: "Feucht",
    MOOD_WET: "Zu nass",
    MOOD_FATAL_WET: "Ertrinkend",
    MOOD_DOUBLE_CRISIS: "Doppelter Notfall",
}

MOOD_EMOJIS: dict[str, str] = {
    MOOD_FREEZE: "🪱🥶",
    MOOD_COLD: "🪱🧥",
    MOOD_COOL: "🪱🙂",
    MOOD_COMFORT: "🪱😄",
    MOOD_WARM: "🪱😅",
    MOOD_HOT: "🪱🥵",
    MOOD_HEAT_DEATH: "🪱🔥",
    MOOD_UNKNOWN: "🪱❓",
    MOOD_FATAL_DRY: "🪱🏜️",
    MOOD_DRY: "🪱💨",
    MOOD_LOW_HUMIDITY: "🪱🥤",
    MOOD_HIGH_HUMIDITY: "🪱💧",
    MOOD_WET: "🪱🌊",
    MOOD_FATAL_WET: "🪱🆘",
    MOOD_DOUBLE_CRISIS: "🪱☠️",
}

MOOD_MESSAGES: dict[str, str] = {
    MOOD_FREEZE: "Notfall: Die Würmer erfrieren, wenn du nicht sofort eingreifst.",
    MOOD_COLD: "Den Würmern ist deutlich zu kalt und sie werden träge.",
    MOOD_COOL: "Etwas frisch, aber noch im tolerierbaren Bereich.",
    MOOD_COMFORT: "So mögen es die Würmer am liebsten.",
    MOOD_WARM: "Schon recht warm, bitte im Blick behalten.",
    MOOD_HOT: "Die Würmer schwitzen bildlich gesprochen schon – jetzt gegensteuern.",
    MOOD_HEAT_DEATH: "Notfall: Akute Überhitzung, sofort kühlen.",
    MOOD_UNKNOWN: "Keine verlässlichen Messdaten verfügbar.",
    MOOD_FATAL_DRY: "Notfall: Das Substrat ist viel zu trocken – die Würmer vertrocknen.",
    MOOD_DRY: "Den Würmern ist es zu trocken – nachfeuchten.",
    MOOD_LOW_HUMIDITY: "Etwas zu trocken, gleich nachsprühen schadet nicht.",
    MOOD_HIGH_HUMIDITY: "Recht feucht, aber noch im grünen Bereich.",
    MOOD_WET: "Zu nass – Sauerstoffmangel droht, trockenes Material untermischen.",
    MOOD_FATAL_WET: "Notfall: Wasserstau – die Würmer ertrinken bzw. ersticken.",
    MOOD_DOUBLE_CRISIS: "Notfall: Mehrere kritische Bedingungen gleichzeitig – sofort eingreifen.",
}

FORECAST_LABELS: dict[str, str] = {
    FORECAST_NONE: "Keine Wetterwarnung",
    FORECAST_COLD: "Kältewarnung",
    FORECAST_FREEZE: "Frostwarnung",
    FORECAST_HEAT: "Hitzewarnung",
    FORECAST_HEAT_DEATH: "Extreme Hitzewarnung",
}

FORECAST_ICONS: dict[str, str] = {
    FORECAST_NONE: "mdi:weather-partly-cloudy",
    FORECAST_COLD: "mdi:snowflake-melt",
    FORECAST_FREEZE: "mdi:snowflake-alert",
    FORECAST_HEAT: "mdi:weather-sunny-alert",
    FORECAST_HEAT_DEATH: "mdi:fire-alert",
}
