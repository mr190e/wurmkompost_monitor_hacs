from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .coordinator import WurmKompostCoordinator


WurmKompostConfigEntry = ConfigEntry[WurmKompostCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: WurmKompostConfigEntry) -> bool:
    """Set up Wurmkompost from a config entry."""
    coordinator = WurmKompostCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    await coordinator.async_start()

    entry.runtime_data = coordinator
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: WurmKompostConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator = entry.runtime_data
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        await coordinator.async_shutdown()
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: WurmKompostConfigEntry) -> None:
    """Reload a config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
