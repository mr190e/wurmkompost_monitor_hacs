from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WurmKompostCoordinator


class WurmKompostEntity(CoordinatorEntity[WurmKompostCoordinator]):
    """Base class for Wurmkompost entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: WurmKompostCoordinator, key: str, name: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{key}"
        self._attr_name = name

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
            name=self.coordinator.compost_name,
            manufacturer="Custom / HACS",
            model="Wurmkompost Monitor",
            configuration_url="https://github.com/mr190e/wurmkompost_monitor_hacs",
        )
