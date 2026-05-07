from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import FORECAST_ICONS, HUMIDITY_ICONS, STATUS_ICONS
from .coordinator import WurmKompostCoordinator
from .entity import WurmKompostEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wurmkompost sensors."""
    coordinator: WurmKompostCoordinator = entry.runtime_data
    entities: list[SensorEntity] = [
        WurmCurrentTemperatureSensor(coordinator),
        WurmStatusSensor(coordinator),
        WurmMoodSensor(coordinator),
        WurmEmojiSensor(coordinator),
        WurmForecastWarningSensor(coordinator),
        WurmForecastMinSensor(coordinator),
        WurmForecastMaxSensor(coordinator),
    ]
    if coordinator.humidity_entity:
        entities.extend(
            [
                WurmCurrentHumiditySensor(coordinator),
                WurmHumidityStatusSensor(coordinator),
            ]
        )
    async_add_entities(entities)


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


class WurmCurrentHumiditySensor(WurmKompostEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_suggested_display_precision = 1

    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "current_humidity", "Feuchtigkeit")
        self._attr_icon = "mdi:water-percent"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.current_humidity

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "quelle": self.coordinator.data.humidity_entity,
            "status": self.coordinator.data.humidity_status_label,
            "farbe": self.coordinator.data.humidity_color,
            "empfehlung": self.coordinator.data.humidity_recommendation,
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
            "feuchtigkeit_prozent": self.coordinator.data.current_humidity,
            "feuchtigkeit_status": self.coordinator.data.humidity_status_label,
            "feuchtigkeit_typ": self.coordinator.data.humidity_sensor_type_label,
            "empfehlung": self.coordinator.data.recommendation,
            "feuchtigkeit_empfehlung": self.coordinator.data.humidity_recommendation,
            "temperatursensor": self.coordinator.data.temperature_entity,
            "feuchtigkeitssensor": self.coordinator.data.humidity_entity,
            "wetter_entity": self.coordinator.data.weather_entity,
            "sonnen_exposition": self.coordinator.data.sun_exposure_label,
            "vorwarnung": self.coordinator.data.forecast_warning_label,
            "prognose_minimum_c": self.coordinator.data.forecast_min_c,
            "prognose_maximum_c": self.coordinator.data.forecast_max_c,
            "prognose_maximum_ambient_c": self.coordinator.data.forecast_max_ambient_c,
            "prognose_maximum_sonnenzuschlag_c": self.coordinator.data.forecast_max_sun_uplift_c,
            "prognose_minimum_zeit": self.coordinator.data.forecast_min_at,
            "prognose_maximum_zeit": self.coordinator.data.forecast_max_at,
            "farbe": self.coordinator.data.status_color,
            "wurm_emoji": self.coordinator.data.mood_emoji,
            "wurmstimmung": self.coordinator.data.mood_label,
            "wurm_botschaft": self.coordinator.data.mood_message,
        }


class WurmHumidityStatusSensor(WurmKompostEntity, SensorEntity):
    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "humidity_status", "Feuchtigkeitsstatus")

    @property
    def native_value(self) -> str:
        return self.coordinator.data.humidity_status_label

    @property
    def icon(self) -> str:
        return HUMIDITY_ICONS[self.coordinator.data.humidity_status_key]

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "feuchtigkeit_prozent": self.coordinator.data.current_humidity,
            "empfehlung": self.coordinator.data.humidity_recommendation,
            "feuchtigkeitssensor": self.coordinator.data.humidity_entity,
            "farbe": self.coordinator.data.humidity_color,
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
            "feuchtigkeit_status": self.coordinator.data.humidity_status_label,
            "farbe": self.coordinator.data.status_color,
            "feuchtigkeit_farbe": self.coordinator.data.humidity_color,
            "empfehlung": self.coordinator.data.recommendation,
            "feuchtigkeit_empfehlung": self.coordinator.data.humidity_recommendation,
        }


class WurmEmojiSensor(WurmKompostEntity, SensorEntity):
    _attr_entity_registry_enabled_default = False
    _attr_entity_category = EntityCategory.DIAGNOSTIC

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
            "feuchtigkeit_status": self.coordinator.data.humidity_status_label,
            "temperatur_c": self.coordinator.data.current_temp_c,
            "feuchtigkeit_prozent": self.coordinator.data.current_humidity,
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
            "forecast_maximum_ambient_c": self.coordinator.data.forecast_max_ambient_c,
            "forecast_maximum_sonnenzuschlag_c": self.coordinator.data.forecast_max_sun_uplift_c,
            "forecast_maximum_wetter": self.coordinator.data.forecast_max_condition,
            "forecast_minimum_in_stunden": self.coordinator.data.hours_to_forecast_min,
            "forecast_maximum_in_stunden": self.coordinator.data.hours_to_forecast_max,
            "forecast_minimum_zeit": self.coordinator.data.forecast_min_at,
            "forecast_maximum_zeit": self.coordinator.data.forecast_max_at,
            "sonnen_exposition": self.coordinator.data.sun_exposure_label,
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
            "ambient_c": self.coordinator.data.forecast_max_ambient_c,
            "sonnenzuschlag_c": self.coordinator.data.forecast_max_sun_uplift_c,
            "wetter": self.coordinator.data.forecast_max_condition,
            "sonnen_exposition": self.coordinator.data.sun_exposure_label,
        }
