from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import FORECAST_ICONS, STATUS_ICONS
from .coordinator import WurmKompostCoordinator
from .entity import WurmKompostEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wurmkompost sensors."""
    coordinator: WurmKompostCoordinator = entry.runtime_data
    async_add_entities(
        [
            WurmCurrentTemperatureSensor(coordinator),
            WurmStatusSensor(coordinator),
            WurmMoodSensor(coordinator),
            WurmEmojiSensor(coordinator),
            WurmForecastWarningSensor(coordinator),
            WurmForecastMinSensor(coordinator),
            WurmForecastMaxSensor(coordinator),
        ]
    )


class WurmCurrentTemperatureSensor(WurmKompostEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision = 1

    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "current_temp", "Temperatur")
        self._attr_icon = "mdi:thermometer"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.current_temp_c

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "quelle": self.coordinator.data.temperature_entity,
            "status": self.coordinator.data.status_label,
            "farbe": self.coordinator.data.status_color,
            "wurm_emoji": self.coordinator.data.mood_emoji,
            "wurmstimmung": self.coordinator.data.mood_label,
        }


class WurmStatusSensor(WurmKompostEntity, SensorEntity):
    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "status", "Status")

    @property
    def native_value(self) -> str:
        return self.coordinator.data.status_label

    @property
    def icon(self) -> str:
        return STATUS_ICONS[self.coordinator.data.status_key]

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "temperature_c": self.coordinator.data.current_temp_c,
            "empfehlung": self.coordinator.data.recommendation,
            "temperatursensor": self.coordinator.data.temperature_entity,
            "wetter_entity": self.coordinator.data.weather_entity,
            "vorwarnung": self.coordinator.data.forecast_warning_label,
            "prognose_minimum_c": self.coordinator.data.forecast_min_c,
            "prognose_maximum_c": self.coordinator.data.forecast_max_c,
            "prognose_minimum_zeit": self.coordinator.data.forecast_min_at,
            "prognose_maximum_zeit": self.coordinator.data.forecast_max_at,
            "farbe": self.coordinator.data.status_color,
            "wurm_emoji": self.coordinator.data.mood_emoji,
            "wurmstimmung": self.coordinator.data.mood_label,
            "wurm_botschaft": self.coordinator.data.mood_message,
        }


class WurmMoodSensor(WurmKompostEntity, SensorEntity):
    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "mood", "Wurmstimmung")
        self._attr_icon = "mdi:emoticon-excited-outline"

    @property
    def native_value(self) -> str:
        return self.coordinator.data.mood_label

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "emoji": self.coordinator.data.mood_emoji,
            "botschaft": self.coordinator.data.mood_message,
            "status": self.coordinator.data.status_label,
            "farbe": self.coordinator.data.status_color,
            "empfehlung": self.coordinator.data.recommendation,
        }


class WurmEmojiSensor(WurmKompostEntity, SensorEntity):
    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "emoji", "Wurmgesicht")
        self._attr_icon = "mdi:worm"

    @property
    def native_value(self) -> str:
        return self.coordinator.data.mood_emoji

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "wurmstimmung": self.coordinator.data.mood_label,
            "botschaft": self.coordinator.data.mood_message,
            "status": self.coordinator.data.status_label,
            "temperatur_c": self.coordinator.data.current_temp_c,
            "farbe": self.coordinator.data.status_color,
        }


class WurmForecastWarningSensor(WurmKompostEntity, SensorEntity):
    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "forecast_warning", "Wetterwarnung")

    @property
    def native_value(self) -> str:
        return self.coordinator.data.forecast_warning_label

    @property
    def icon(self) -> str:
        return FORECAST_ICONS[self.coordinator.data.forecast_warning_key]

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "forecast_minimum_c": self.coordinator.data.forecast_min_c,
            "forecast_maximum_c": self.coordinator.data.forecast_max_c,
            "forecast_minimum_in_stunden": self.coordinator.data.hours_to_forecast_min,
            "forecast_maximum_in_stunden": self.coordinator.data.hours_to_forecast_max,
            "forecast_minimum_zeit": self.coordinator.data.forecast_min_at,
            "forecast_maximum_zeit": self.coordinator.data.forecast_max_at,
        }


class WurmForecastMinSensor(WurmKompostEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision = 1

    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "forecast_min", "Prognose Minimum")
        self._attr_icon = "mdi:thermometer-low"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.forecast_min_c

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "zeit": self.coordinator.data.forecast_min_at,
            "in_stunden": self.coordinator.data.hours_to_forecast_min,
        }


class WurmForecastMaxSensor(WurmKompostEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision = 1

    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "forecast_max", "Prognose Maximum")
        self._attr_icon = "mdi:thermometer-high"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.forecast_max_c

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "zeit": self.coordinator.data.forecast_max_at,
            "in_stunden": self.coordinator.data.hours_to_forecast_max,
        }
