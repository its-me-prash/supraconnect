"""Sensor entities for Supra Connect."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DESCRIPTOR_HINTS, DOMAIN, EMPTY_DESCRIPTOR_HINT
from .coordinator import SupraConnectCoordinator
from .entity import SupraConnectEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up dynamic Supra Connect sensors."""

    coordinator: SupraConnectCoordinator = hass.data[DOMAIN][entry.entry_id]
    known: set[tuple[str, str]] = set()

    @callback
    def add_sensor(vin: str, key: str) -> None:
        if (vin, key) in known:
            return
        known.add((vin, key))
        async_add_entities([SupraConnectSensor(coordinator, vin, key)])

    coordinator.async_register_discovery_callback("sensor", add_sensor)


class SupraConnectSensor(SupraConnectEntity, SensorEntity):
    """Dynamic telemetry sensor."""

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""

        return self.coordinator.vehicles[self.vin].values.get(self.key)

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Return a guessed unit for known descriptors."""

        return self._hint.unit

    @property
    def device_class(self) -> SensorDeviceClass | str | None:
        """Return a guessed sensor device class."""

        if self._hint.device_class is None:
            return None
        try:
            return SensorDeviceClass(self._hint.device_class)
        except ValueError:
            return self._hint.device_class

    @property
    def state_class(self) -> SensorStateClass | str | None:
        """Return the state class."""

        if self._hint.state_class is None:
            return None
        try:
            return SensorStateClass(self._hint.state_class)
        except ValueError:
            return self._hint.state_class

    @property
    def _hint(self):
        compact_key = self.key.lower().replace("_", "").replace("-", "")
        for fragment, hint in DESCRIPTOR_HINTS.items():
            if fragment in compact_key:
                return hint
        return EMPTY_DESCRIPTOR_HINT
