<p align="center">
  <img src="https://raw.githubusercontent.com/its-me-prash/supraconnect/master/custom_components/supraconnect/logo.png" alt="Supra Connect" width="180">
</p>

<h1 align="center">Supra Connect</h1>

<p align="center">
  <strong>Home Assistant Integration für Toyota Supra Connect Telemetrie</strong>
</p>

<p align="center">
  <a href="https://hacs.xyz"><img src="https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge" alt="HACS"></a>
  <a href="https://github.com/its-me-prash/supraconnect/releases"><img src="https://img.shields.io/github/v/release/its-me-prash/supraconnect?include_prereleases&style=for-the-badge" alt="Version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/Lizenz-Apache%202.0-blue.svg?style=for-the-badge" alt="Lizenz"></a>
  <a href="https://www.home-assistant.io"><img src="https://img.shields.io/badge/Home%20Assistant-2025.3%2B-blue?style=for-the-badge" alt="Home Assistant"></a>
  <a href="https://github.com/its-me-prash/supraconnect/actions/workflows/validate.yml"><img src="https://img.shields.io/github/actions/workflow/status/its-me-prash/supraconnect/validate.yml?branch=master&style=for-the-badge&label=Validate" alt="Validate"></a>
</p>

---

**Supra Connect** verbindet Home Assistant mit Toyota-Supra-Connect-kompatibler Telemetrie. Die erste Alpha ist bewusst
read-only und nutzt MQTT/Cardata-artige Payloads, damit reale Supra-Daten lokal getestet werden können, ohne den seit
2025 blockierten MyBMW-App-API-Weg wieder als Produktionsbasis einzubauen.

> **Alpha-Status:** `v1.0.0-alpha.x` ist für lokale Validierung mit dem eigenen Supra gedacht. Danach folgt `beta` für
> ausgewählte Home-Assistant-Tester und erst danach `v1.0.0` als stabile öffentliche Version.

## Aktueller Stand & ehrliche Limits (v1.0.0-alpha.3)

Supra Connect ist eine neue, eigenständige HACS-Integration. Der alte Fork-Kontext wurde als historische Quelle
aufgeräumt; die aktive Codebasis liegt unter `custom_components/supraconnect`.

### Was jetzt funktioniert

- HACS-kompatible Repository-Struktur mit `hacs.json`
- Home-Assistant-Config-Flow
- MQTT-Subscription auf frei konfigurierbare Topic-Präfixe, Standard: `bmw/`
- VIN-Erkennung aus Payload oder Topic
- dynamische Sensoren aus eingehenden Telemetrie-Deskriptoren
- dynamische Binary-Sensoren für boolesche Zustände
- Device Tracker, sobald Latitude/Longitude-Telemetrie vorhanden ist
- Logo-Assets für README, HACS-Ansicht und Integration

### Was noch in Arbeit ist

- echte Supra-Descriptor-Mappings mit schöneren Entity-Namen, Units und Device Classes
- Diagnostics/Repair-Flows für stale MQTT-Daten und ungültige Payloads
- robuste Tests mit echten, anonymisierten Supra-Payloads
- optionaler BMW/Supra-CarData-Setup-Guide mit klaren Screenshots
- direkte Supra-Connect-Auth nur, wenn ein stabiler und supportbarer Weg verifiziert ist

### Bewusste Limits

- keine Remote-Kommandos in Alpha
- kein Versuch, die blockierte MyBMW-App-API als Standardpfad wiederzubeleben
- MQTT/Cardata-Bridge oder kompatibler Datenstrom wird vorausgesetzt
- Payload-Formate können sich in Alpha noch ändern

## Unterstützte Plattformen

```text
sensor  |  binary_sensor  |  device_tracker
```

---

## Telemetrie & Entities

Die Integration ist descriptor-first: neue Werte aus deinem Payload werden automatisch als Entities angelegt.

### Beispiel-Payload

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

Nested JSON wird automatisch geflattet. VIN kann im Payload oder im MQTT-Topic stehen.

### MQTT Topic

| Feld | Standard | Beschreibung |
|---|---:|---|
| Topic-Präfix | `bmw/` | Die Integration subscribed auf `<prefix>#` |
| VIN | Payload oder Topic | 17-stellige VIN, z. B. `<prefix><VIN>` |
| Payload | JSON | `data`-Objekt oder direktes Descriptor-Objekt |

---

## Installation

### HACS

1. HACS -> Integrationen -> drei Punkte -> Benutzerdefinierte Repositories
2. URL: `https://github.com/its-me-prash/supraconnect` -> Kategorie: Integration
3. **Supra Connect** installieren
4. Home Assistant neu starten
5. Einstellungen -> Geräte & Dienste -> Integration hinzufügen -> **Supra Connect**

### Manuell

```bash
cp -r custom_components/supraconnect ~/.homeassistant/custom_components/
```

Home Assistant danach neu starten.

---

## Konfiguration

| Feld | Pflicht | Beschreibung |
|---|---|---|
| Name | ja | Anzeigename der Integration |
| MQTT-Topic-Präfix | ja | Präfix deines Supra/BMW-CarData-MQTT-Streams, Standard `bmw/` |

---

## Technischer Hintergrund

Toyota Supra Connect basiert auf BMW ConnectedDrive. Seit dem 29.09.2025 blockiert BMW Drittzugriffe auf den alten
MyBMW-App-API-Weg, der früher von `bimmer_connected` und ähnlichen Integrationen genutzt wurde. Deshalb startet dieses
Projekt nicht mit einem alten Login-Flow, sondern mit einem ehrlichen Telemetriepfad über MQTT/Cardata-kompatible Daten.

```text
custom_components/supraconnect/
  config_flow.py      -> UI-Setup
  coordinator.py      -> MQTT ingest, VIN discovery, descriptor flattening
  sensor.py           -> dynamische Sensoren
  binary_sensor.py    -> dynamische Binary-Sensoren
  device_tracker.py   -> GPS-Tracker bei vorhandenen Koordinaten
  entity.py           -> gemeinsame Entity-Basis
```

- keine externen Python-Abhängigkeiten
- Home-Assistant-MQTT-Integration als Transport
- read-only Alpha für sichere reale Fahrzeugvalidierung

---

## Roadmap

| Phase | Ziel |
|---|---|
| `v1.0.0-alpha.x` | lokale Validierung mit dem eigenen Supra, Payload-Sammlung, Descriptor-Mapping |
| `v1.0.0-beta.x` | ausgewählte Home-Assistant-Tester, stabilere Entity-Namen, Migrationen |
| `v1.0.0` | öffentliche stabile HACS-Version |

Details: [VERSIONING.md](VERSIONING.md)

---

## Attribution

Dieses Projekt ist ein eigenständiges Community-Projekt von `its-me-prash`. Der ursprüngliche Fork-Kontext diente nur
als historische Quelle für BMW/Supra-Plattformwissen. Details: [ATTRIBUTION.md](ATTRIBUTION.md)

---

## Lizenz

Apache License 2.0 - [LICENSE](LICENSE)

Dieses Projekt ist nicht mit Toyota, BMW, BMW ConnectedDrive oder Supra Connect offiziell verbunden.
