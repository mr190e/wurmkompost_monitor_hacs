from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import logging
from typing import Any, Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_UNIT_OF_MEASUREMENT, UnitOfTemperature
from homeassistant.core import Event, EventStateChangedData, HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util
from homeassistant.util.unit_conversion import TemperatureConverter

from .const import (
    CONDITION_SUN_FACTOR,
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
    DEFAULT_CONDITION_SUN_FACTOR,
    DEFAULT_FATAL_HEAT_TEMP,
    DEFAULT_FORECAST_HOURS,
    DEFAULT_FREEZE_TEMP,
    DEFAULT_HEAT_WARNING_TEMP,
    DEFAULT_HUMIDITY_COMFORT_MAX,
    DEFAULT_HUMIDITY_COMFORT_MIN,
    DEFAULT_HUMIDITY_DRY,
    DEFAULT_HUMIDITY_FATAL_DRY,
    DEFAULT_HUMIDITY_FATAL_WET,
    DEFAULT_HUMIDITY_SENSOR_TYPE,
    DEFAULT_HUMIDITY_WET,
    DEFAULT_SUN_EXPOSURE,
    DEFAULT_SUN_UPLIFT_FULL_SUN,
    DEFAULT_SUN_UPLIFT_PARTIAL_SHADE,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_WARM_TEMP,
    FORECAST_COLD,
    FORECAST_FREEZE,
    FORECAST_HEAT,
    FORECAST_HEAT_DEATH,
    FORECAST_LABELS,
    FORECAST_NONE,
    HUMIDITY_COLORS,
    HUMIDITY_COMFORT,
    HUMIDITY_DRY,
    HUMIDITY_FATAL_DRY,
    HUMIDITY_FATAL_WET,
    HUMIDITY_HIGH,
    HUMIDITY_LABELS,
    HUMIDITY_LOW,
    HUMIDITY_NOT_CONFIGURED,
    HUMIDITY_RECOMMENDATIONS,
    HUMIDITY_SEVERITY,
    HUMIDITY_TYPE_LABELS,
    HUMIDITY_UNKNOWN,
    HUMIDITY_WET,
    MOOD_BY_HUMIDITY,
    MOOD_BY_STATUS,
    MOOD_COMFORT,
    MOOD_DOUBLE_CRISIS,
    MOOD_EMOJIS,
    MOOD_LABELS,
    MOOD_MESSAGES,
    MOOD_UNKNOWN,
    STATUS_COLD,
    STATUS_COLORS,
    STATUS_COMFORT,
    STATUS_COOL,
    STATUS_FREEZE,
    STATUS_HEAT_DEATH,
    STATUS_HOT,
    STATUS_LABELS,
    STATUS_RECOMMENDATIONS,
    STATUS_UNKNOWN,
    STATUS_WARM,
    SUN_EXPOSURE_FULL_SUN,
    SUN_EXPOSURE_LABELS,
    SUN_EXPOSURE_PARTIAL_SHADE,
    SUN_EXPOSURE_SHADE,
    SUN_HOUR_FACTORS,
    TEMP_SEVERITY,
)

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class WurmKompostData:
    """Runtime data for the Wurmkompost integration."""

    compost_name: str
    temperature_entity: str
    humidity_entity: str | None
    weather_entity: str
    current_temp_c: float | None
    current_temp_source_unit: str | None
    current_humidity: float | None
    current_humidity_source_unit: str | None
    status_key: str
    status_label: str
    recommendation: str
    status_color: str
    humidity_status_key: str
    humidity_status_label: str
    humidity_recommendation: str
    humidity_color: str
    mood_key: str
    mood_label: str
    mood_emoji: str
    mood_message: str
    forecast_warning_key: str
    forecast_warning_label: str
    forecast_min_c: float | None
    forecast_max_c: float | None
    forecast_min_ambient_c: float | None
    forecast_max_ambient_c: float | None
    forecast_max_sun_uplift_c: float | None
    forecast_max_condition: str | None
    forecast_min_at: str | None
    forecast_max_at: str | None
    hours_to_forecast_min: float | None
    hours_to_forecast_max: float | None
    sun_exposure_key: str
    sun_exposure_label: str
    humidity_sensor_type_key: str
    humidity_sensor_type_label: str
    frost_alarm: bool
    heat_alarm: bool
    dry_alarm: bool
    wet_alarm: bool
    forecast_cold_warning: bool
    forecast_heat_warning: bool


class WurmKompostCoordinator(DataUpdateCoordinator[WurmKompostData]):
    """Coordinate Wurmkompost data updates."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.config_entry = entry
        self._unsubscribers: list[Callable[[], None]] = []

        super().__init__(
            hass,
            _LOGGER,
            name=f"wurmkompost_{entry.entry_id}",
            update_interval=DEFAULT_UPDATE_INTERVAL,
        )

    @property
    def compost_name(self) -> str:
        return str(self._get_option(CONF_COMPOST_NAME, DEFAULT_COMPOST_NAME))

    @property
    def temperature_entity(self) -> str:
        return str(self._get_option(CONF_TEMPERATURE_SENSOR, ""))

    @property
    def humidity_entity(self) -> str | None:
        value = self._get_option(CONF_HUMIDITY_SENSOR, "")
        return str(value) if value else None

    @property
    def weather_entity(self) -> str:
        return str(self._get_option(CONF_WEATHER_ENTITY, ""))

    @property
    def sun_exposure(self) -> str:
        value = str(self._get_option(CONF_SUN_EXPOSURE, DEFAULT_SUN_EXPOSURE))
        if value not in SUN_EXPOSURE_LABELS:
            return DEFAULT_SUN_EXPOSURE
        return value

    @property
    def humidity_sensor_type(self) -> str:
        value = str(self._get_option(CONF_HUMIDITY_SENSOR_TYPE, DEFAULT_HUMIDITY_SENSOR_TYPE))
        if value not in HUMIDITY_TYPE_LABELS:
            return DEFAULT_HUMIDITY_SENSOR_TYPE
        return value

    async def async_start(self) -> None:
        """Start listeners for faster updates."""

        @callback
        def _handle_source_change(event: Event[EventStateChangedData]) -> None:
            entity_id = event.data["entity_id"]
            _LOGGER.debug("Source entity changed: %s", entity_id)
            self.hass.async_create_task(self.async_request_refresh())

        tracked = [self.temperature_entity, self.weather_entity]
        if self.humidity_entity:
            tracked.append(self.humidity_entity)

        self._unsubscribers.append(
            async_track_state_change_event(
                self.hass,
                tracked,
                _handle_source_change,
            )
        )

    async def async_shutdown(self) -> None:
        """Cancel listeners when unloading."""
        while self._unsubscribers:
            unsubscribe = self._unsubscribers.pop()
            unsubscribe()

    async def _async_update_data(self) -> WurmKompostData:
        """Fetch and normalize current compost and forecast data."""
        current_state = self.hass.states.get(self.temperature_entity)
        if current_state is None:
            raise UpdateFailed(f"Temperature entity not found: {self.temperature_entity}")

        current_temp_c = _state_to_celsius(
            current_state.state, current_state.attributes.get(ATTR_UNIT_OF_MEASUREMENT)
        )
        status_key = self._classify_current_temp(current_temp_c)

        current_humidity: float | None = None
        humidity_source_unit: str | None = None
        humidity_status_key = HUMIDITY_NOT_CONFIGURED

        if self.humidity_entity:
            humidity_state = self.hass.states.get(self.humidity_entity)
            if humidity_state is None:
                _LOGGER.warning("Humidity entity not found: %s", self.humidity_entity)
                humidity_status_key = HUMIDITY_UNKNOWN
            else:
                humidity_source_unit = humidity_state.attributes.get(ATTR_UNIT_OF_MEASUREMENT)
                current_humidity = _state_to_percent(humidity_state.state)
                humidity_status_key = self._classify_humidity(current_humidity)

        mood_key = self._combined_mood_key(status_key, humidity_status_key)

        forecast_min_c: float | None = None
        forecast_max_c: float | None = None
        forecast_min_ambient_c: float | None = None
        forecast_max_ambient_c: float | None = None
        forecast_max_sun_uplift_c: float | None = None
        forecast_max_condition: str | None = None
        forecast_min_at: str | None = None
        forecast_max_at: str | None = None
        hours_to_forecast_min: float | None = None
        hours_to_forecast_max: float | None = None
        forecast_warning_key = FORECAST_NONE

        weather_state = self.hass.states.get(self.weather_entity)
        weather_unit = weather_state.attributes.get("temperature_unit") if weather_state else None

        try:
            response = await self.hass.services.async_call(
                "weather",
                "get_forecasts",
                {
                    "entity_id": [self.weather_entity],
                    "type": "hourly",
                },
                blocking=True,
                return_response=True,
            )
        except Exception as err:  # pragma: no cover - defensive for runtime HA differences
            _LOGGER.warning("Unable to fetch weather forecast for %s: %s", self.weather_entity, err)
            response = None

        forecast_items = []
        if isinstance(response, dict):
            forecast_items = response.get(self.weather_entity, {}).get("forecast", []) or []

        forecast_hours = int(self._get_option(CONF_FORECAST_HOURS, DEFAULT_FORECAST_HOURS))
        sliced_items = forecast_items[:forecast_hours]

        exposure = self.sun_exposure
        max_uplift_full = float(
            self._get_option(CONF_SUN_UPLIFT_FULL_SUN, DEFAULT_SUN_UPLIFT_FULL_SUN)
        )
        max_uplift_partial = float(
            self._get_option(CONF_SUN_UPLIFT_PARTIAL_SHADE, DEFAULT_SUN_UPLIFT_PARTIAL_SHADE)
        )

        converted_forecasts: list[tuple[datetime | None, float, float, float, str | None]] = []
        for item in sliced_items:
            raw_temp = item.get("temperature")
            ambient_c = _to_celsius(raw_temp, weather_unit)
            if ambient_c is None:
                continue
            when = dt_util.parse_datetime(item.get("datetime")) if item.get("datetime") else None
            condition = item.get("condition")
            uplift = _sun_uplift(when, condition, exposure, max_uplift_full, max_uplift_partial)
            adjusted = ambient_c + uplift
            converted_forecasts.append((when, adjusted, ambient_c, uplift, condition))

        if converted_forecasts:
            # Cold warnings are based on ambient (sun does not warm at night), heat warnings on adjusted.
            min_item = min(converted_forecasts, key=lambda item: item[2])
            max_item = max(converted_forecasts, key=lambda item: item[1])
            forecast_min_c = round(min_item[2], 1)
            forecast_min_ambient_c = forecast_min_c
            forecast_max_c = round(max_item[1], 1)
            forecast_max_ambient_c = round(max_item[2], 1)
            forecast_max_sun_uplift_c = round(max_item[3], 1)
            forecast_max_condition = max_item[4]
            forecast_min_at = min_item[0].isoformat() if min_item[0] else None
            forecast_max_at = max_item[0].isoformat() if max_item[0] else None
            hours_to_forecast_min = _hours_until(min_item[0])
            hours_to_forecast_max = _hours_until(max_item[0])
            forecast_warning_key = self._classify_forecast(forecast_min_c, forecast_max_c)

        return WurmKompostData(
            compost_name=self.compost_name,
            temperature_entity=self.temperature_entity,
            humidity_entity=self.humidity_entity,
            weather_entity=self.weather_entity,
            current_temp_c=None if current_temp_c is None else round(current_temp_c, 1),
            current_temp_source_unit=current_state.attributes.get(ATTR_UNIT_OF_MEASUREMENT),
            current_humidity=None if current_humidity is None else round(current_humidity, 1),
            current_humidity_source_unit=humidity_source_unit,
            status_key=status_key,
            status_label=STATUS_LABELS[status_key],
            recommendation=STATUS_RECOMMENDATIONS[status_key],
            status_color=STATUS_COLORS[status_key],
            humidity_status_key=humidity_status_key,
            humidity_status_label=HUMIDITY_LABELS[humidity_status_key],
            humidity_recommendation=HUMIDITY_RECOMMENDATIONS[humidity_status_key],
            humidity_color=HUMIDITY_COLORS[humidity_status_key],
            mood_key=mood_key,
            mood_label=MOOD_LABELS[mood_key],
            mood_emoji=MOOD_EMOJIS[mood_key],
            mood_message=MOOD_MESSAGES[mood_key],
            forecast_warning_key=forecast_warning_key,
            forecast_warning_label=FORECAST_LABELS[forecast_warning_key],
            forecast_min_c=forecast_min_c,
            forecast_max_c=forecast_max_c,
            forecast_min_ambient_c=forecast_min_ambient_c,
            forecast_max_ambient_c=forecast_max_ambient_c,
            forecast_max_sun_uplift_c=forecast_max_sun_uplift_c,
            forecast_max_condition=forecast_max_condition,
            forecast_min_at=forecast_min_at,
            forecast_max_at=forecast_max_at,
            hours_to_forecast_min=hours_to_forecast_min,
            hours_to_forecast_max=hours_to_forecast_max,
            sun_exposure_key=exposure,
            sun_exposure_label=SUN_EXPOSURE_LABELS[exposure],
            humidity_sensor_type_key=self.humidity_sensor_type,
            humidity_sensor_type_label=HUMIDITY_TYPE_LABELS[self.humidity_sensor_type],
            frost_alarm=status_key == STATUS_FREEZE,
            heat_alarm=status_key == STATUS_HEAT_DEATH,
            dry_alarm=humidity_status_key == HUMIDITY_FATAL_DRY,
            wet_alarm=humidity_status_key == HUMIDITY_FATAL_WET,
            forecast_cold_warning=forecast_warning_key in {FORECAST_COLD, FORECAST_FREEZE},
            forecast_heat_warning=forecast_warning_key in {FORECAST_HEAT, FORECAST_HEAT_DEATH},
        )

    def _classify_current_temp(self, current_temp_c: float | None) -> str:
        """Classify the current compost temperature."""
        if current_temp_c is None:
            return STATUS_UNKNOWN

        freeze_temp = float(self._get_option(CONF_FREEZE_TEMP, DEFAULT_FREEZE_TEMP))
        cold_temp = float(self._get_option(CONF_COLD_TEMP, DEFAULT_COLD_TEMP))
        comfort_min = float(self._get_option(CONF_COMFORT_MIN_TEMP, DEFAULT_COMFORT_MIN_TEMP))
        comfort_max = float(self._get_option(CONF_COMFORT_MAX_TEMP, DEFAULT_COMFORT_MAX_TEMP))
        warm_temp = float(self._get_option(CONF_WARM_TEMP, DEFAULT_WARM_TEMP))
        fatal_heat_temp = float(self._get_option(CONF_FATAL_HEAT_TEMP, DEFAULT_FATAL_HEAT_TEMP))

        if current_temp_c <= freeze_temp:
            return STATUS_FREEZE
        if current_temp_c < cold_temp:
            return STATUS_COLD
        if current_temp_c < comfort_min:
            return STATUS_COOL
        if current_temp_c <= comfort_max:
            return STATUS_COMFORT
        if current_temp_c <= warm_temp:
            return STATUS_WARM
        if current_temp_c <= fatal_heat_temp:
            return STATUS_HOT
        return STATUS_HEAT_DEATH

    def _classify_humidity(self, humidity: float | None) -> str:
        """Classify the current substrate humidity."""
        if humidity is None:
            return HUMIDITY_UNKNOWN

        fatal_dry = float(self._get_option(CONF_HUMIDITY_FATAL_DRY, DEFAULT_HUMIDITY_FATAL_DRY))
        dry = float(self._get_option(CONF_HUMIDITY_DRY, DEFAULT_HUMIDITY_DRY))
        comfort_min = float(self._get_option(CONF_HUMIDITY_COMFORT_MIN, DEFAULT_HUMIDITY_COMFORT_MIN))
        comfort_max = float(self._get_option(CONF_HUMIDITY_COMFORT_MAX, DEFAULT_HUMIDITY_COMFORT_MAX))
        wet = float(self._get_option(CONF_HUMIDITY_WET, DEFAULT_HUMIDITY_WET))
        fatal_wet = float(self._get_option(CONF_HUMIDITY_FATAL_WET, DEFAULT_HUMIDITY_FATAL_WET))

        if humidity <= fatal_dry:
            return HUMIDITY_FATAL_DRY
        if humidity < dry:
            return HUMIDITY_DRY
        if humidity < comfort_min:
            return HUMIDITY_LOW
        if humidity <= comfort_max:
            return HUMIDITY_COMFORT
        if humidity <= wet:
            return HUMIDITY_HIGH
        if humidity < fatal_wet:
            return HUMIDITY_WET
        return HUMIDITY_FATAL_WET

    def _combined_mood_key(self, status_key: str, humidity_key: str) -> str:
        """Combine temperature- and humidity-based moods, picking the worst."""
        temp_severity = TEMP_SEVERITY.get(status_key, 0)
        humidity_severity = HUMIDITY_SEVERITY.get(humidity_key, 0)

        if status_key == STATUS_UNKNOWN and humidity_key in {HUMIDITY_NOT_CONFIGURED, HUMIDITY_UNKNOWN}:
            return MOOD_UNKNOWN

        # Two simultaneous critical conditions get a special "double crisis" mood.
        if temp_severity >= 3 and humidity_severity >= 3:
            return MOOD_DOUBLE_CRISIS

        if humidity_severity > temp_severity:
            return MOOD_BY_HUMIDITY[humidity_key]

        if temp_severity > humidity_severity:
            return MOOD_BY_STATUS[status_key]

        # Equal severity: prefer the actual deviation (humidity reported, then temp).
        if humidity_severity > 0 and humidity_key not in {HUMIDITY_UNKNOWN, HUMIDITY_NOT_CONFIGURED}:
            return MOOD_BY_HUMIDITY[humidity_key]

        return MOOD_BY_STATUS.get(status_key, MOOD_COMFORT)

    def _classify_forecast(self, forecast_min_c: float | None, forecast_max_c: float | None) -> str:
        """Classify forecast-based warnings."""
        freeze_temp = float(self._get_option(CONF_FREEZE_TEMP, DEFAULT_FREEZE_TEMP))
        cold_warning_buffer = float(
            self._get_option(CONF_COLD_WARNING_BUFFER, DEFAULT_COLD_WARNING_BUFFER)
        )
        heat_warning_temp = float(self._get_option(CONF_HEAT_WARNING_TEMP, DEFAULT_HEAT_WARNING_TEMP))
        fatal_heat_temp = float(self._get_option(CONF_FATAL_HEAT_TEMP, DEFAULT_FATAL_HEAT_TEMP))

        if forecast_min_c is not None and forecast_min_c <= freeze_temp:
            return FORECAST_FREEZE
        if forecast_max_c is not None and forecast_max_c > fatal_heat_temp:
            return FORECAST_HEAT_DEATH
        if forecast_min_c is not None and forecast_min_c <= freeze_temp + cold_warning_buffer:
            return FORECAST_COLD
        if forecast_max_c is not None and forecast_max_c >= heat_warning_temp:
            return FORECAST_HEAT
        return FORECAST_NONE

    def _get_option(self, key: str, default: Any) -> Any:
        """Get a config value with options overriding data."""
        return self.config_entry.options.get(key, self.config_entry.data.get(key, default))


def _normalize_unit(unit: str | None) -> str | None:
    if unit is None:
        return None
    normalized = str(unit).strip().lower()
    if normalized in {"°c", "c", "celsius"}:
        return UnitOfTemperature.CELSIUS
    if normalized in {"°f", "f", "fahrenheit"}:
        return UnitOfTemperature.FAHRENHEIT
    return None


def _to_celsius(value: Any, unit: str | None) -> float | None:
    """Convert a temperature value to celsius."""
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None

    normalized = _normalize_unit(unit)
    if normalized is None or normalized == UnitOfTemperature.CELSIUS:
        return numeric

    return float(TemperatureConverter.convert(numeric, normalized, UnitOfTemperature.CELSIUS))


def _state_to_celsius(state: str | None, unit: str | None) -> float | None:
    if state in {None, "unknown", "unavailable", "none"}:
        return None
    return _to_celsius(state, unit)


def _state_to_percent(state: str | None) -> float | None:
    """Parse a humidity/moisture state as percent. Accepts 0-1 or 0-100 ranges."""
    if state in {None, "unknown", "unavailable", "none"}:
        return None
    try:
        numeric = float(state)
    except (TypeError, ValueError):
        return None
    # Some sensors emit a 0..1 fraction instead of 0..100. Normalize.
    if 0 <= numeric <= 1:
        return numeric * 100.0
    return numeric


def _hours_until(when: datetime | None) -> float | None:
    if when is None:
        return None
    now = dt_util.now()
    return round((when - now).total_seconds() / 3600, 1)


def _sun_uplift(
    when: datetime | None,
    condition: str | None,
    exposure: str,
    max_uplift_full_sun: float,
    max_uplift_partial_shade: float,
) -> float:
    """Estimate °C added to ambient air temp due to direct sun on the bin."""
    if when is None or exposure == SUN_EXPOSURE_SHADE:
        return 0.0
    if exposure == SUN_EXPOSURE_FULL_SUN:
        max_uplift = max_uplift_full_sun
    elif exposure == SUN_EXPOSURE_PARTIAL_SHADE:
        max_uplift = max_uplift_partial_shade
    else:
        return 0.0
    local_dt = dt_util.as_local(when)
    hour_factor = SUN_HOUR_FACTORS.get(local_dt.hour, 0.0)
    if hour_factor == 0.0:
        return 0.0
    cloud_factor = (
        CONDITION_SUN_FACTOR.get(condition, DEFAULT_CONDITION_SUN_FACTOR)
        if condition is not None
        else DEFAULT_CONDITION_SUN_FACTOR
    )
    return max(0.0, max_uplift * hour_factor * cloud_factor)
