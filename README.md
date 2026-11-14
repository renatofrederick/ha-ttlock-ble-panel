# TTLock BLE Panel Bridge

Private HACS integration that adds `ttlock_ble_panel.get_passcodes` for the
Access Panel without replacing or patching the official `ttlock_ble` integration.

## Security boundary

The service returns real PINs only in the response to an authenticated Home
Assistant service call. It does not create entities, write state, history,
diagnostics, or logs. Anyone permitted to call this Home Assistant service can
receive those PINs; use a dedicated, restricted Home Assistant token for the
Access Panel and do not publish this repository.

## Installation

Add this private GitHub repository to HACS as a custom Integration repository,
install it, then add **TTLock BLE Panel Bridge** once under Settings → Devices
& services. The official `ttlock_ble` integration stays installed and is not
modified. Restart Home Assistant only when performing this installation.

The paired Access Panel version uses `ttlock_ble_panel.get_passcodes` for read
and synchronization. It intentionally does not enable creating or deleting PINs.

## Compatibility

Tested against `ha-ttlock-ble` `v3.12.2`. The bridge reads that integration's
live runtime connection, which is not a public upstream API. If a later TTLock
BLE update changes it, reads fail safely with a clear Home Assistant error; the
lock itself and its official integration remain unaffected.
