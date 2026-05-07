from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback

from .const import (
    CONF_COLD_TEMP,
    CONF_COLD_WARNING_BUFFER,
    CONF_COMFORT_MAX_TEMP,
    CONF_COMFORT_MIN_TEMP,
    CONF_COMPOST_NAME,
    CONF_FATAL_HEAT_TEMP,
    CONF_FORECAST_HOURS,
    CONF_FREEZE_TEMP,
    CONF_HEAT_WARNING_TEMP,
    CONF_HUMIDITY_COMFORT_MAX,
    CONF_HUMIDITY_COMFORT_MIN,
    CONF_HUMIDITY_DRY,
    CONF_HUMIDITY_FATAL_DRY,
    CONF_HUMIDITY_FATAL_WET,
    CONF_HUMIDITY_SENSOR,
    CONF_HUMIDITY_SENSOR_TYPE,
    CONF_HUMIDITY_WET,
    CONF_SUN_EXPOSURE,
    CONF_SUN_UPLIFT_FULL_SUN,
    CONF_SUN_UPLIFT_PARTIAL_SHADE,
    CONF_TEMPERATURE_SENSOR,
    CONF_WARM_TEMP,
    CONF_WEATHER_ENTITY,
    DEFAULT_COLD_TEMP,
    DEFAULT_COLD_WARNING_BUFFER,
    DEFAULT_COMFORT_MAX_TEMP,
    DEFAULT_COMFORT_MIN_TEMP,
    DEFAULT_COMPOST_NAME,
    DEFAULT_FATAL_HEAT_TEMP,
    DEFAULT_FORECAST_HOURS,
    DEFAULT_FREEZE_TEMP,
    DEFAULT_HEAT_WARNING_TEMP,
    DEFAULT_HUMIDITY_SENSOR_TYPE,
    DEFAULT_SUN_EXPOSURE,
    DEFAULT_SUN_UPLIFT_FULL_SUN,
    DEFAULT_SUN_UPLIFT_PARTIAL_SHADE,
    DEFAULT_WARM_TEMP,
    DOMAIN,
    HUMIDITY_DEFAULTS_BY_TYPE,
    HUMIDITY_TYPE_LABELS,
    SUN_EXPOSURE_LABELS,
)

NO_HUMIDITY_SENSOR = "__no_humidity__"


def _friendly_entity_map(hass: HomeAssistant, domain: str, *, temperature_only: bool = False) -> dict[str, str]:
    entities: dict[str, str] = {}
    for state in sorted(hass.states.async_all(domain), key=lambda item: item.name.lower()):
        if temperature_only:
            device_class = str(state.attributes.get("device_class", "")).lower()
            unit = str(state.attributes.get("unit_of_measurement", "")).lower()
            if device_class != "temperature" and unit not in {"°c", "°f", "c", "f"}:
                continue
        label = f"{state.name} ({state.entity_id})"
        entities[state.entity_id] = label
    return entities


def _humidity_entity_map(hass: HomeAssistant) -> dict[str, str]:
    entities: dict[str, str] = {NO_HUMIDITY_SENSOR: "– kein Feuchtigkeitssensor –"}
    for state in sorted(hass.states.async_all("sensor"), key=lambda item: item.name.lower()):
        device_class = str(state.attributes.get("device_class", "")).lower()
        unit = str(state.attributes.get("unit_of_measurement", "")).lower()
        if device_class not in {"humidity", "moisture"} and unit not in {"%", "% rh", "%rh"}:
            continue
        entities[state.entity_id] = f"{state.name} ({state.entity_id})"
    return entities


class WurmKompostConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Wurmkompost."""

    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):
        errors: dict[str, str] = {}

        temp_entities = _friendly_entity_map(self.hass, "sensor", temperature_only=True)
        weather_entities = _friendly_entity_map(self.hass, "weather")
        humidity_entities = _humidity_entity_map(self.hass)

        if not temp_entities:
            return self.async_abort(reason="no_temperature_sensors")
        if not weather_entities:
            return self.async_abort(reason="no_weather_entities")

        if user_input is not None:
            await self.async_set_unique_id(
                f"{user_input[CONF_TEMPERATURE_SENSOR]}::{user_input[CONF_WEATHER_ENTITY]}"
            )
            self._abort_if_unique_id_configured()

            humidity_choice = user_input.get(CONF_HUMIDITY_SENSOR, NO_HUMIDITY_SENSOR)
            humidity_value = "" if humidity_choice == NO_HUMIDITY_SENSOR else humidity_choice
            humidity_type = user_input.get(CONF_HUMIDITY_SENSOR_TYPE, DEFAULT_HUMIDITY_SENSOR_TYPE)

            data = {
                CONF_COMPOST_NAME: user_input[CONF_NAME],
                CONF_TEMPERATURE_SENSOR: user_input[CONF_TEMPERATURE_SENSOR],
                CONF_HUMIDITY_SENSOR: humidity_value,
                CONF_HUMIDITY_SENSOR_TYPE: humidity_type,
                CONF_WEATHER_ENTITY: user_input[CONF_WEATHER_ENTITY],
                CONF_SUN_EXPOSURE: user_input.get(CONF_SUN_EXPOSURE, DEFAULT_SUN_EXPOSURE),
            }
            # Pre-seed humidity thresholds with sensible defaults for the chosen sensor type.
            if humidity_value:
                data.update(HUMIDITY_DEFAULTS_BY_TYPE.get(humidity_type, {}))
            return self.async_create_entry(title=user_input[CONF_NAME], data=data)

        defaults = {
            CONF_NAME: DEFAULT_COMPOST_NAME,
            CONF_TEMPERATURE_SENSOR: next(iter(temp_entities)),
            CONF_HUMIDITY_SENSOR: NO_HUMIDITY_SENSOR,
            CONF_HUMIDITY_SENSOR_TYPE: DEFAULT_HUMIDITY_SENSOR_TYPE,
            CONF_WEATHER_ENTITY: next(iter(weather_entities)),
            CONF_SUN_EXPOSURE: DEFAULT_SUN_EXPOSURE,
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default=defaults[CONF_NAME]): str,
                    vol.Required(
                        CONF_TEMPERATURE_SENSOR,
                        default=defaults[CONF_TEMPERATURE_SENSOR],
                    ): vol.In(temp_entities),
                    vol.Required(
                        CONF_HUMIDITY_SENSOR,
                        default=defaults[CONF_HUMIDITY_SENSOR],
                    ): vol.In(humidity_entities),
                    vol.Required(
                        CONF_HUMIDITY_SENSOR_TYPE,
                        default=defaults[CONF_HUMIDITY_SENSOR_TYPE],
                    ): vol.In(HUMIDITY_TYPE_LABELS),
                    vol.Required(
                        CONF_WEATHER_ENTITY,
                        default=defaults[CONF_WEATHER_ENTITY],
                    ): vol.In(weather_entities),
                    vol.Required(
                        CONF_SUN_EXPOSURE,
                        default=defaults[CONF_SUN_EXPOSURE],
                    ): vol.In(SUN_EXPOSURE_LABELS),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Create the options flow."""
        return WurmKompostOptionsFlow(config_entry)


class WurmKompostOptionsFlow(OptionsFlow):
    """Handle options for Wurmkompost."""

    def __init__(self, config_entry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None):
        temp_entities = _friendly_entity_map(self.hass, "sensor", temperature_only=True)
        weather_entities = _friendly_entity_map(self.hass, "weather")
        humidity_entities = _humidity_entity_map(self.hass)

        current_temp = self._value(CONF_TEMPERATURE_SENSOR, None)
        current_humidity = self._value(CONF_HUMIDITY_SENSOR, "")
        current_weather = self._value(CONF_WEATHER_ENTITY, None)
        if current_temp and current_temp not in temp_entities:
            temp_entities[current_temp] = current_temp
        if current_humidity and current_humidity not in humidity_entities:
            humidity_entities[current_humidity] = current_humidity
        if current_weather and current_weather not in weather_entities:
            weather_entities[current_weather] = current_weather

        if user_input is not None:
            humidity_choice = user_input.get(CONF_HUMIDITY_SENSOR, NO_HUMIDITY_SENSOR)
            if humidity_choice == NO_HUMIDITY_SENSOR:
                user_input[CONF_HUMIDITY_SENSOR] = ""
            return self.async_create_entry(title="", data=user_input)

        humidity_default = current_humidity if current_humidity else NO_HUMIDITY_SENSOR
        humidity_type_default = self._value(CONF_HUMIDITY_SENSOR_TYPE, DEFAULT_HUMIDITY_SENSOR_TYPE)
        type_defaults = HUMIDITY_DEFAULTS_BY_TYPE.get(
            humidity_type_default, HUMIDITY_DEFAULTS_BY_TYPE[DEFAULT_HUMIDITY_SENSOR_TYPE]
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_COMPOST_NAME,
                        default=self._value(CONF_COMPOST_NAME, DEFAULT_COMPOST_NAME),
                    ): str,
                    vol.Required(
                        CONF_TEMPERATURE_SENSOR,
                        default=self._value(CONF_TEMPERATURE_SENSOR, next(iter(temp_entities))),
                    ): vol.In(temp_entities),
                    vol.Required(
                        CONF_HUMIDITY_SENSOR,
                        default=humidity_default,
                    ): vol.In(humidity_entities),
                    vol.Required(
                        CONF_HUMIDITY_SENSOR_TYPE,
                        default=humidity_type_default,
                    ): vol.In(HUMIDITY_TYPE_LABELS),
                    vol.Required(
                        CONF_WEATHER_ENTITY,
                        default=self._value(CONF_WEATHER_ENTITY, next(iter(weather_entities))),
                    ): vol.In(weather_entities),
                    vol.Required(
                        CONF_SUN_EXPOSURE,
                        default=self._value(CONF_SUN_EXPOSURE, DEFAULT_SUN_EXPOSURE),
                    ): vol.In(SUN_EXPOSURE_LABELS),
                    vol.Required(
                        CONF_FREEZE_TEMP,
                        default=self._value(CONF_FREEZE_TEMP, DEFAULT_FREEZE_TEMP),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_COLD_TEMP,
                        default=self._value(CONF_COLD_TEMP, DEFAULT_COLD_TEMP),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_COMFORT_MIN_TEMP,
                        default=self._value(CONF_COMFORT_MIN_TEMP, DEFAULT_COMFORT_MIN_TEMP),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_COMFORT_MAX_TEMP,
                        default=self._value(CONF_COMFORT_MAX_TEMP, DEFAULT_COMFORT_MAX_TEMP),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_WARM_TEMP,
                        default=self._value(CONF_WARM_TEMP, DEFAULT_WARM_TEMP),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_FATAL_HEAT_TEMP,
                        default=self._value(CONF_FATAL_HEAT_TEMP, DEFAULT_FATAL_HEAT_TEMP),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_FORECAST_HOURS,
                        default=self._value(CONF_FORECAST_HOURS, DEFAULT_FORECAST_HOURS),
                    ): vol.All(vol.Coerce(int), vol.Range(min=1, max=24)),
                    vol.Required(
                        CONF_COLD_WARNING_BUFFER,
                        default=self._value(CONF_COLD_WARNING_BUFFER, DEFAULT_COLD_WARNING_BUFFER),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_HEAT_WARNING_TEMP,
                        default=self._value(CONF_HEAT_WARNING_TEMP, DEFAULT_HEAT_WARNING_TEMP),
                    ): vol.Coerce(float),
                    vol.Required(
                        CONF_SUN_UPLIFT_FULL_SUN,
                        default=self._value(CONF_SUN_UPLIFT_FULL_SUN, DEFAULT_SUN_UPLIFT_FULL_SUN),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0, max=30)),
                    vol.Required(
                        CONF_SUN_UPLIFT_PARTIAL_SHADE,
                        default=self._value(
                            CONF_SUN_UPLIFT_PARTIAL_SHADE, DEFAULT_SUN_UPLIFT_PARTIAL_SHADE
                        ),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0, max=30)),
                    vol.Required(
                        CONF_HUMIDITY_FATAL_DRY,
                        default=self._value(
                            CONF_HUMIDITY_FATAL_DRY, type_defaults[CONF_HUMIDITY_FATAL_DRY]
                        ),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0, max=100)),
                    vol.Required(
                        CONF_HUMIDITY_DRY,
                        default=self._value(CONF_HUMIDITY_DRY, type_defaults[CONF_HUMIDITY_DRY]),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0, max=100)),
                    vol.Required(
                        CONF_HUMIDITY_COMFORT_MIN,
                        default=self._value(
                            CONF_HUMIDITY_COMFORT_MIN, type_defaults[CONF_HUMIDITY_COMFORT_MIN]
                        ),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0, max=100)),
                    vol.Required(
                        CONF_HUMIDITY_COMFORT_MAX,
                        default=self._value(
                            CONF_HUMIDITY_COMFORT_MAX, type_defaults[CONF_HUMIDITY_COMFORT_MAX]
                        ),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0, max=100)),
                    vol.Required(
                        CONF_HUMIDITY_WET,
                        default=self._value(CONF_HUMIDITY_WET, type_defaults[CONF_HUMIDITY_WET]),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0, max=100)),
                    vol.Required(
                        CONF_HUMIDITY_FATAL_WET,
                        default=self._value(
                            CONF_HUMIDITY_FATAL_WET, type_defaults[CONF_HUMIDITY_FATAL_WET]
                        ),
                    ): vol.All(vol.Coerce(float), vol.Range(min=0, max=100)),
                }
            ),
        )

    def _value(self, key: str, default):
        return self.config_entry.options.get(key, self.config_entry.data.get(key, default))
