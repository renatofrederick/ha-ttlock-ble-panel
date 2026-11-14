"""Config flow for the private TTLock BLE Panel Bridge."""

from __future__ import annotations

from homeassistant import config_entries

from .const import DOMAIN


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Set up the one local bridge entry."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Create the bridge without collecting or storing credentials."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return self.async_create_entry(title="TTLock BLE Panel Bridge", data={})
