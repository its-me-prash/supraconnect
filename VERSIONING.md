# Versioning

Supra Connect uses Semantic Versioning for releases.

## Development Phases

### Alpha

Tags: `v1.0.0-alpha.N`

Alpha releases are for private/local development with the maintainer's own Supra. Breaking changes are expected. The
integration may change entity names, payload mapping, setup flow behavior, and storage details without migration support.

Use alpha while validating the core loop:

- HACS installability
- Home Assistant config flow
- MQTT/Cardata payload ingestion
- VIN/device discovery
- dynamic telemetry entities
- real vehicle behavior from the maintainer's own Supra

### Beta

Tags: `v1.0.0-beta.N`

Beta releases are for selected Home Assistant users. The integration should be installable, documented, and useful, but
may still need descriptor mapping fixes for different vehicles, regions, and MQTT bridge payloads.

Beta changes should avoid unnecessary breaking changes and should include migrations when practical.

### Stable

Tags: `v1.0.0`, then normal SemVer such as `v1.1.0` and `v1.1.1`

Stable releases are public releases for general HACS users. Breaking changes require a major version bump.

## Version Rules

- Increment alpha builds as `v1.0.0-alpha.1`, `v1.0.0-alpha.2`, and so on.
- Move to beta only after the maintainer's local Supra setup is reliable.
- Move to stable only after external Home Assistant testers confirm setup, telemetry, and update behavior.
- Use patch releases for bug fixes after stable.
- Use minor releases for backward-compatible features after stable.
- Use major releases for breaking changes after stable.
