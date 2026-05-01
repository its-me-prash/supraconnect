"""Binary sensor entities for Supra Connect."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import BINARY_KEY_PARTS, DOMAIN
from .coordinator import SupraConnectCoordinator
from .entity import SupraConnectEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up dynamic Supra Connect binary sensors."""

    coordinator: SupraConnectCoordinator = hass.data[DOMAIN][entry.entry_id]
    known: set[tuple[str, str]] = set()

    @callback
    def add_binary_sensor(vin: str, key: str) -> None:
        if (vin, key) in known:
            return
        known.add((vin, key))
        async_add_entities([SupraConnectBinarySensor(coordinator, vin, key)])

    coordinator.async_register_discovery_callback("binary_sensor", add_binary_sensor)


class SupraConnectBinarySensor(SupraConnectEntity, BinarySensorEntity):
    """Dynamic binary telemetry sensor."""

    @property
    def is_on(self) -> bool | None:
        """Return the binary state."""

        value = self.coordinator.vehicles[self.vin].values.get(self.key)
        return bool(value) if value is not None else None

    @property
    def device_class(self) -> BinarySensorDeviceClass | None:
        """Return a guessed binary sensor device class."""

        key = self.key.lower()
        if "door" in key or "window" in key or "hood" in key or "trunk" in key or "tailgate" in key:
            return BinarySensorDeviceClass.OPENING
        if "lock" in key or "secure" in key:
            return BinarySensorDeviceClass.LOCK
        if "charging" in key or "connected" in key:
            return BinarySensorDeviceClass.PLUG
        if "moving" in key:
            return BinarySensorDeviceClass.MOVING
        return None

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Only expose plausible binary descriptors by default."""

        compact_key = self.key.lower().replace("_", "").replace("-", "")
        return any(part in compact_key for part in BINARY_KEY_PARTS)
