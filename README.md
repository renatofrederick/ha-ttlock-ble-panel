# TTLock BLE Panel Bridge

[Leia em Português (Brasil)](README.pt-BR.md)

Private HACS integration that adds `ttlock_ble_panel.get_passcodes` to the
Access Panel without replacing, copying, or modifying the official
`ttlock_ble` integration.

## What it does

- Restores only PIN reading and synchronization for the Access Panel.
- Does not enable PIN creation, modification, or deletion.
- Leaves the official `ttlock_ble` integration independently updatable through
  HACS.

## HACS installation

1. Confirm the official **TTLock BLE** integration is installed, loaded, and
   has the lock's `lock.*` entity.
2. In HACS, open the three-dot menu and select **Custom repositories**.
3. Add this private repository URL with the **Integration** category. The GitHub
   account connected to HACS must have access to this repository.
4. Find and install **TTLock BLE Panel Bridge** in HACS.
5. Restart Home Assistant once to load the component.
6. Go to **Settings → Devices & services → Add integration** and add
   **TTLock BLE Panel Bridge**. No token, password, or extra configuration is
   required.
7. Update the Access Panel with the `ttlock-panel-read-adapter` branch, which
   uses `ttlock_ble_panel.get_passcodes`.

The panel can then list and synchronize PINs read via BLE. Test a manual read
on a lock you administer before promoting the Access Panel update.

## Security

The service returns real PINs only in the response to an authenticated Home
Assistant service call. It does not create entities or write entity state,
history, diagnostics, or logs. Anyone authorized to call this service can read
the PINs; use a dedicated Home Assistant credential with the least compatible
privilege for the Access Panel and keep this repository private.

## Updates and rollback

- Update the bridge normally through HACS; the official `ttlock_ble`
  integration is independent.
- Before updating, note the installed bridge version. If an update fails, use
  HACS **Redownload** to select a prior available release, then restart Home
  Assistant.
- To remove the bridge, remove its configuration entry under **Devices &
  services**, then uninstall it through HACS. This does not remove locks,
  entities, or history owned by `ttlock_ble`.

## Compatibility

Tested against `ha-ttlock-ble` `v3.12.2`. The bridge reads that integration's
live runtime connection, which is not a public upstream API. If a later TTLock
BLE update changes it, reads fail with a clear Home Assistant error; the lock
and official integration remain unaffected.
