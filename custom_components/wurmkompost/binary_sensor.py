from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import HUMIDITY_DRY, HUMIDITY_WET
from .coordinator import WurmKompostCoordinator
from .entity import WurmKompostEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Wurmkompost binary sensors."""
    coordinator: WurmKompostCoordinator = entry.runtime_data
    entities: list[BinarySensorEntity] = [
        WurmFrostAlarmBinarySensor(coordinator),
        WurmHeatAlarmBinarySensor(coordinator),
        WurmForecastColdWarningBinarySensor(coordinator),
        WurmForecastHeatWarningBinarySensor(coordinator),
    ]
    if coordinator.humidity_entity:
        entities.extend(
            [
                WurmDryAlarmBinarySensor(coordinator),
                WurmWetAlarmBinarySensor(coordinator),
                WurmDryWarningBinarySensor(coordinator),
                WurmWetWarningBinarySensor(coordinator),
            ]
        )
    async_add_entities(entities)


class _WurmProblemBinarySensor(WurmKompostEntity, BinarySensorEntity):
    _attr_device_class = BinarySensorDeviceClass.PROBLEM


class WurmFrostAlarmBinarySensor(_WurmProblemBinarySensor):
    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "frost_alarm", "Frostalarm")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.frost_alarm

    @property
    def icon(self) -> str:
        return "mdi:snowflake-alert" if self.is_on else "mdi:snowflake-off"

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "status": self.coordinator.data.status_label,
            "temperature_c": self.coordinator.data.current_temp_c,
        }


class WurmHeatAlarmBinarySensor(_WurmProblemBinarySensor):
    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "heat_alarm", "Hitzealarm")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.heat_alarm

    @property
    def icon(self) -> str:
        return "mdi:fire-alert" if self.is_on else "mdi:fire-off"

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "status": self.coordinator.data.status_label,
            "temperature_c": self.coordinator.data.current_temp_c,
        }


class WurmDryAlarmBinarySensor(_WurmProblemBinarySensor):
    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "dry_alarm", "Vertrocknungsalarm")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.dry_alarm

    @property
    def icon(self) -> str:
        return "mdi:water-off" if self.is_on else "mdi:water-check"

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "feuchtigkeit_status": self.coordinator.data.humidity_status_label,
            "feuchtigkeit_prozent": self.coordinator.data.current_humidity,
            "empfehlung": self.coordinator.data.humidity_recommendation,
        }


class WurmWetAlarmBinarySensor(_WurmProblemBinarySensor):
    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "wet_alarm", "Ertrinkungsalarm")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.wet_alarm

    @property
    def icon(self) -> str:
        return "mdi:water-alert" if self.is_on else "mdi:water-check"

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "feuchtigkeit_status": self.coordinator.data.humidity_status_label,
            "feuchtigkeit_prozent": self.coordinator.data.current_humidity,
            "empfehlung": self.coordinator.data.humidity_recommendation,
        }


class WurmDryWarningBinarySensor(_WurmProblemBinarySensor):
    """Soft warning before the substrate hits the fatal-dry threshold."""

    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "dry_warning", "Trockenwarnung")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.humidity_status_key == HUMIDITY_DRY

    @property
    def icon(self) -> str:
        return "mdi:water-minus" if self.is_on else "mdi:water-check"

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "feuchtigkeit_status": self.coordinator.data.humidity_status_label,
            "feuchtigkeit_prozent": self.coordinator.data.current_humidity,
            "empfehlung": self.coordinator.data.humidity_recommendation,
        }


class WurmWetWarningBinarySensor(_WurmProblemBinarySensor):
    """Soft warning before the substrate hits the fatal-wet threshold."""

    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "wet_warning", "Nasswarnung")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.humidity_status_key == HUMIDITY_WET

    @property
    def icon(self) -> str:
        return "mdi:water-plus" if self.is_on else "mdi:water-check"

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "feuchtigkeit_status": self.coordinator.data.humidity_status_label,
            "feuchtigkeit_prozent": self.coordinator.data.current_humidity,
            "empfehlung": self.coordinator.data.humidity_recommendation,
        }


class WurmForecastColdWarningBinarySensor(_WurmProblemBinarySensor):
    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "forecast_cold_warning", "Kältewarnung")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.forecast_cold_warning

    @property
    def icon(self) -> str:
        return "mdi:snowflake-melt" if self.is_on else "mdi:weather-cloudy"

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "warnung": self.coordinator.data.forecast_warning_label,
            "prognose_minimum_c": self.coordinator.data.forecast_min_c,
            "prognose_minimum_zeit": self.coordinator.data.forecast_min_at,
        }


class WurmForecastHeatWarningBinarySensor(_WurmProblemBinarySensor):
    def __init__(self, coordinator: WurmKompostCoordinator) -> None:
        super().__init__(coordinator, "forecast_heat_warning", "Hitzewarnung")

    @property
    def is_on(self) -> bool:
        return self.coordinator.data.forecast_heat_warning

    @property
    def icon(self) -> str:
        return "mdi:weather-sunny-alert" if self.is_on else "mdi:white-balance-sunny"

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "warnung": self.coordinator.data.forecast_warning_label,
            "prognose_maximum_c": self.coordinator.data.forecast_max_c,
            "prognose_maximum_zeit": self.coordinator.data.forecast_max_at,
        }
