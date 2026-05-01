"""Constants for the Supra Connect integration."""

from __future__ import annotations

from dataclasses import dataclass

DOMAIN = "supraconnect"
CONF_TOPIC_PREFIX = "topic_prefix"
DEFAULT_TOPIC_PREFIX = "bmw/"
PLATFORMS = ["sensor", "binary_sensor", "device_tracker"]

ATTR_SOURCE_TOPIC = "source_topic"
ATTR_UPDATED_AT = "updated_at"
ATTR_VIN = "vin"

LOCATION_LAT_KEYS = (
    "vehicle.location.coordinates.latitude",
    "vehicle.location.latitude",
    "location.coordinates.latitude",
    "location.latitude",
    "latitude",
    "lat",
)

LOCATION_LON_KEYS = (
    "vehicle.location.coordinates.longitude",
    "vehicle.location.longitude",
    "location.coordinates.longitude",
    "location.longitude",
    "longitude",
    "lon",
    "lng",
)


@dataclass(frozen=True)
class DescriptorHint:
    """Metadata hint for a dynamic telemetry descriptor."""

    unit: str | None = None
    device_class: str | None = None
    state_class: str | None = None


DESCRIPTOR_HINTS: dict[str, DescriptorHint] = {
    "mileage": DescriptorHint("km", "distance", "total_increasing"),
    "odometer": DescriptorHint("km", "distance", "total_increasing"),
    "remainingrange": DescriptorHint("km", "distance"),
    "remainingfuel": DescriptorHint("L", None),
    "fuel.level": DescriptorHint("%", "battery"),
    "charging.power": DescriptorHint("kW", "power"),
    "stateofcharge": DescriptorHint("%", "battery"),
    "soc": DescriptorHint("%", "battery"),
    "battery": DescriptorHint("%", "battery"),
    "temperature": DescriptorHint("°C", "temperature"),
    "pressure": DescriptorHint("kPa", "pressure"),
}
EMPTY_DESCRIPTOR_HINT = DescriptorHint()

BINARY_KEY_PARTS = (
    "isopen",
    "islocked",
    "issecure",
    "isactive",
    "isconnected",
    "ismoving",
    "charging.status",
)
