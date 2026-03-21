from __future__ import annotations

from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "wurmkompost"
PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

CONF_COMPOST_NAME = "compost_name"
CONF_TEMPERATURE_SENSOR = "temperature_sensor"
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

DEFAULT_UPDATE_INTERVAL = timedelta(minutes=15)

STATUS_FREEZE = "alarm_erfrieren"
STATUS_COLD = "zu_kalt"
STATUS_COOL = "kuehl"
STATUS_COMFORT = "wohlfuehlbereich"
STATUS_WARM = "warm"
STATUS_HOT = "zu_warm"
STATUS_HEAT_DEATH = "alarm_hitzetod"
STATUS_UNKNOWN = "unbekannt"

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

MOOD_LABELS: dict[str, str] = {
    MOOD_FREEZE: "Erfrierend",
    MOOD_COLD: "Frierend",
    MOOD_COOL: "Fröstelnd",
    MOOD_COMFORT: "Zufrieden",
    MOOD_WARM: "Leicht warm",
    MOOD_HOT: "Schwitzend",
    MOOD_HEAT_DEATH: "Notfall",
    MOOD_UNKNOWN: "Unklar",
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
