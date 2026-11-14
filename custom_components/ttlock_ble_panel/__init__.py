"""Private Home Assistant bridge for the Access Panel."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from .const import DOMAIN, SERVICE_GET_PASSCODES
from .services import async_register_services


async def async_setup_entry(hass: HomeAssistant, entry) -> bool:
    """Set up the bridge without modifying the official TTLock integration."""
    await async_register_services(hass)
    return True


async def async_unload_entry(hass: HomeAssistant, entry) -> bool:
    """Remove the bridge service when its sole config entry is removed."""
    hass.services.async_remove(DOMAIN, SERVICE_GET_PASSCODES)
    return True
