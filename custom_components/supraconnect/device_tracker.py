"""Device tracker entities for Supra Connect."""

from __future__ import annotations

from typing import Any

from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, LOCATION_LAT_KEYS, LOCATION_LON_KEYS
from .coordinator import SupraConnectCoordinator
from .entity import SupraConnectEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up Supra Connect device trackers."""

    coordinator: SupraConnectCoordinator = hass.data[DOMAIN][entry.entry_id]
    known: set[str] = set()

    @callback
    def maybe_add_tracker(vin: str, _key: str) -> None:
        if vin in known:
            return
        state = coordinator.vehicles.get(vin)
        if state is None:
            return
        if find_first_value(state.values, LOCATION_LAT_KEYS) is None:
            return
        if find_first_value(state.values, LOCATION_LON_KEYS) is None:
            return
        known.add(vin)
        async_add_entities([SupraConnectDeviceTracker(coordinator, vin)])

    coordinator.async_register_discovery_callback("sensor", maybe_add_tracker)


class SupraConnectDeviceTracker(SupraConnectEntity, TrackerEntity):
    """Vehicle location tracker."""

    def __init__(self, coordinator: SupraConnectCoordinator, vin: str) -> None:
        super().__init__(coordinator, vin, "location")
        self._attr_unique_id = f"{vin}_location".lower()

    @property
    def latitude(self) -> float | None:
        """Return latitude."""

        return as_float(find_first_value(self.coordinator.vehicles[self.vin].values, LOCATION_LAT_KEYS))

    @property
    def longitude(self) -> float | None:
        """Return longitude."""

        return as_float(find_first_value(self.coordinator.vehicles[self.vin].values, LOCATION_LON_KEYS))

    @property
    def source_type(self) -> str:
        """Return tracker source type."""

        return "gps"

    @property
    def available(self) -> bool:
        """Return if GPS data is available."""

        return self.latitude is not None and self.longitude is not None


def find_first_value(values: dict[str, Any], keys: tuple[str, ...]) -> Any:
    """Find the first present value by exact or suffix descriptor key."""

    lowered = {key.lower(): value for key, value in values.items()}
    for key in keys:
        if key in lowered:
            return lowered[key]
    for descriptor, value in lowered.items():
        if any(descriptor.endswith(key) for key in keys):
            return value
    return None


def as_float(value: Any) -> float | None:
    """Convert a telemetry value to float."""

    try:
        return float(value)
    except (TypeError, ValueError):
        return None
