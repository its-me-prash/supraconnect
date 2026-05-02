# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| `v1.0.0-alpha.x` | alpha testing only |

## Reporting a Vulnerability

Please do not open public issues for vulnerabilities that expose credentials, tokens, precise location data, or other
private vehicle/account data.

Report security-sensitive findings privately to the repository maintainer through GitHub.

## Scope

Security-sensitive examples include:

- leaking MQTT credentials
- logging access tokens or refresh tokens
- exposing precise GPS data in diagnostics
- unsafe remote-command behavior if such functionality is added later
