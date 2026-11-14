"""Private response-only service bridging TTLock BLE to the Access Panel."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall, SupportsResponse
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry

from .const import DOMAIN, SERVICE_GET_PASSCODES, TTLOCK_BLE_DOMAIN


def _date_value(value: date | datetime | str | None) -> str | None:
    """Serialize a schedule boundary without widening the response surface."""
    if value is None or isinstance(value, str):
        return value
    return value.isoformat()


def _serialize(entry: Any) -> dict[str, Any]:
    """Return only the PIN and schedule fields required by the panel."""
    return {
        "passcode": entry.passcode,
        "pwd_type": entry.pwd_type.name,
        "start_date": _date_value(entry.start_date),
        "end_date": _date_value(entry.end_date),
    }


def _connection_for_lock_entity(hass: HomeAssistant, entity_id: str) -> Any:
    """Resolve an official TTLock BLE lock entity to its live connection."""
    if not entity_id.startswith("lock."):
        raise HomeAssistantError("entity_id must be a TTLock BLE lock entity")

    entity = async_get_entity_registry(hass).async_get(entity_id)
    if entity is None or entity.device_id is None:
        raise HomeAssistantError(f"No TTLock BLE device found for {entity_id}")
    device = async_get_device_registry(hass).async_get(entity.device_id)
    if device is None:
        raise HomeAssistantError(f"No TTLock BLE device found for {entity_id}")
    mac = next(
        (
            identifier
            for domain, identifier in device.identifiers
            if domain == TTLOCK_BLE_DOMAIN
        ),
        None,
    )
    if mac is None:
        raise HomeAssistantError(f"No TTLock BLE lock found for {entity_id}")

    for entry in hass.config_entries.async_entries(TTLOCK_BLE_DOMAIN):
        runtime_data = getattr(entry, "runtime_data", None)
        for connection_mac, connection in getattr(runtime_data, "connections", {}).items():
            if connection_mac.lower() == mac.lower():
                return connection
    raise HomeAssistantError(f"No active TTLock BLE connection found for {entity_id}")


async def async_register_services(hass: HomeAssistant) -> None:
    """Register the bridge service once per Home Assistant process."""
    if hass.services.has_service(DOMAIN, SERVICE_GET_PASSCODES):
        return

    async def handle_get_passcodes(call: ServiceCall) -> dict[str, list[dict[str, Any]]]:
        connection = _connection_for_lock_entity(hass, call.data["entity_id"])
        entries = await connection.async_get_passcodes()
        if entries is None:
            raise HomeAssistantError("Unable to read passcodes from the lock")
        # PINs are returned only to this caller; never log, dispatch, or store them.
        return {"passcodes": [_serialize(entry) for entry in entries]}

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_PASSCODES,
        handle_get_passcodes,
        schema=vol.Schema({vol.Required("entity_id"): cv.entity_id}),
        supports_response=SupportsResponse.ONLY,
    )
