# Privacy

Supra Connect is designed as a local Home Assistant integration.

## Data Flow

- MQTT telemetry is consumed from the Home Assistant MQTT integration.
- The integration does not send vehicle telemetry to this repository, GitHub, or any maintainer-controlled service.
- VIN, GPS coordinates, mileage, and status values remain inside the user's Home Assistant instance unless the user
  explicitly shares logs or diagnostics.

## Sensitive Data

Before opening issues or sharing payload samples, remove or mask:

- VIN
- precise GPS coordinates
- account identifiers
- access tokens or refresh tokens
- license plates
- home/work addresses

## Alpha Testing

During alpha, payload examples are especially useful, but they should be anonymized before being posted publicly.
