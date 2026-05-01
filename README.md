# Supra Connect for Home Assistant

<p align="center">
  <img src="images/logo.png" alt="Toyota Supra Connect logo" width="180">
</p>

Custom Home Assistant integration for Toyota Supra Connect telemetry.

This is an independent Supra Connect project by `its-me-prash`. It was initially cleaned out of a fork that contained
`bimmer_connected` code and fixtures, but it is not intended as a continuation of `bimmer_connected`. The old repository
was used as historical reference material for the BMW/Supra platform context; the integration code in this repository is
now a new Home Assistant HACS integration focused on Supra Connect telemetry.

Toyota Supra Connect is powered by BMW ConnectedDrive. Since September 29, 2025 BMW blocks the old third-party MyBMW API flow that powered `bimmer_connected` and Home Assistant's former BMW Connected Drive integration. This repository therefore starts from a clean HACS integration and uses the currently viable telemetry path: a BMW/Supra-compatible MQTT stream payload, typically produced by a CarData/MQTT bridge.

## Status

- HACS-ready custom integration.
- Config flow in the Home Assistant UI.
- Dynamic vehicle discovery by VIN.
- Dynamic sensors and binary sensors from incoming descriptor payloads.
- Device tracker when latitude/longitude telemetry is present.
- Read-only telemetry first. Remote commands are intentionally not implemented until a reliable official Supra path is verified.

## Installation

1. Add this repository to HACS as a custom repository of type `Integration`.
2. Install `Supra Connect`.
3. Restart Home Assistant.
4. Go to **Settings > Devices & Services > Add Integration > Supra Connect**.
5. Enter the MQTT topic prefix used by your bridge. The default is `bmw/`, which subscribes to `bmw/#`.

## MQTT Payloads

The integration accepts JSON payloads on `<prefix><VIN>` or any subtopic below the prefix. The VIN can be supplied either in the topic or in the payload.

Example:

```json
{
  "vin": "WZ1DB0C00MW000000",
  "data": {
    "vehicle.mileage": 12345,
    "vehicle.state.isVehicleSecure": true,
    "vehicle.location.coordinates.latitude": 52.52,
    "vehicle.location.coordinates.longitude": 13.405
  }
}
```

Nested JSON is flattened automatically, so both descriptor-style payloads and normal nested objects work.

## Why Not Direct Login?

The old `bimmer_connected` MyBMW/Supra API route is not a good production base anymore. Upstream documents that BMW added app-side security checks and blocked third-party requests. Building the HACS integration around that path would look familiar but fail for real users.

This project keeps the first production path honest: ingest official/bridge telemetry into Home Assistant cleanly, then add direct Supra-specific authentication only after it is proven stable and legally usable.

## Roadmap

- Map common Supra descriptors to polished device classes and units.
- Add diagnostics and repair flows for stale MQTT data.
- Add optional known descriptor aliases for nicer entity names.
- Research Supra Connect portal/device auth separately from the blocked MyBMW app flow.

## Release Channels

This project uses SemVer prerelease channels:

- `v1.0.0-alpha.N`: private/local development with the maintainer's own Supra.
- `v1.0.0-beta.N`: wider Home Assistant user testing after the maintainer car setup is stable.
- `v1.0.0`: first public stable release.

See [VERSIONING.md](VERSIONING.md) for the full versioning policy.

## Attribution

See [ATTRIBUTION.md](ATTRIBUTION.md).
