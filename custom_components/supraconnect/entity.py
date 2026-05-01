"""Base entities for Supra Connect."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN
from .coordinator import SupraConnectCoordinator


class SupraConnectEntity(Entity):
    """Base class for Supra Connect entities."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: SupraConnectCoordinator, vin: str, key: str) -> None:
        self.coordinator = coordinator
        self.vin = vin
        self.key = key
        self._attr_unique_id = f"{vin}_{key}".lower().replace(".", "_")
        self._attr_translation_key = "dynamic_descriptor"
        self._attr_translation_placeholders = {"descriptor": key_to_name(key)}

    @property
    def device_info(self) -> DeviceInfo:
        """Return vehicle device info."""

        return DeviceInfo(
            identifiers={(DOMAIN, self.vin)},
            manufacturer="Toyota",
            model="GR Supra",
            name=f"Supra {self.vin[-6:]}",
        )

    @property
    def available(self) -> bool:
        """Return if the entity has data."""

        return self.vin in self.coordinator.vehicles and self.key in self.coordinator.vehicles[self.vin].values

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return common debug attributes."""

        state = self.coordinator.vehicles.get(self.vin)
        if state is None:
            return {}
        return {
            "vin": self.vin,
            "descriptor": self.key,
            "source_topic": state.topics.get(self.key),
            "updated_at": state.updated_at.isoformat() if state.updated_at else None,
        }

    async def async_added_to_hass(self) -> None:
        """Register for coordinator updates."""

        self.async_on_remove(self.coordinator.async_add_listener(self.async_write_ha_state))


def key_to_name(key: str) -> str:
    """Convert descriptor paths to readable names."""

    parts = key.replace("_", ".").split(".")
    cleaned = [part for part in parts if part and part.lower() not in {"vehicle", "data"}]
    return " ".join(split_words(part) for part in cleaned).strip().title()


def split_words(value: str) -> str:
    """Split camelCase-ish descriptor fragments."""

    output = ""
    previous_lower = False
    for char in value:
        if char.isupper() and previous_lower:
            output += " "
        output += char
        previous_lower = char.islower()
    return output
