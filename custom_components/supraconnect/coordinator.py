"""MQTT telemetry coordinator for Supra Connect."""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback

from .const import ATTR_SOURCE_TOPIC, ATTR_UPDATED_AT, ATTR_VIN, CONF_TOPIC_PREFIX

_LOGGER = logging.getLogger(__name__)

VIN_RE = re.compile(r"\b[A-HJ-NPR-Z0-9]{17}\b", re.IGNORECASE)


@dataclass
class VehicleState:
    """Telemetry for one vehicle."""

    vin: str
    values: dict[str, Any] = field(default_factory=dict)
    topics: dict[str, str] = field(default_factory=dict)
    updated_at: datetime | None = None


class SupraConnectCoordinator:
    """Coordinate MQTT messages and dynamic entity discovery."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self.topic_prefix: str = entry.data[CONF_TOPIC_PREFIX]
        self.vehicles: dict[str, VehicleState] = {}
        self._unsubscribe_mqtt: CALLBACK_TYPE | None = None
        self._listeners: list[Callable[[], None]] = []
        self._discovery_callbacks: dict[str, list[Callable[[str, str], None]]] = {
            "sensor": [],
            "binary_sensor": [],
            "device_tracker": [],
        }

    async def async_start(self) -> None:
        """Subscribe to MQTT telemetry."""

        topic = f"{self.topic_prefix}#"
        self._unsubscribe_mqtt = await mqtt.async_subscribe(self.hass, topic, self._async_message_received, 1)
        _LOGGER.info("Subscribed to Supra Connect MQTT topic %s", topic)

    async def async_stop(self) -> None:
        """Stop receiving telemetry."""

        if self._unsubscribe_mqtt is not None:
            self._unsubscribe_mqtt()
            self._unsubscribe_mqtt = None

    @callback
    def async_add_listener(self, update_callback: Callable[[], None]) -> CALLBACK_TYPE:
        """Register an update listener."""

        self._listeners.append(update_callback)

        def remove_listener() -> None:
            self._listeners.remove(update_callback)

        return remove_listener

    @callback
    def async_register_discovery_callback(self, platform: str, add_entity: Callable[[str, str], None]) -> None:
        """Register a callback for dynamic platform entity discovery."""

        self._discovery_callbacks[platform].append(add_entity)
        for vin, state in self.vehicles.items():
            for key in state.values:
                if self.platform_for_key(key, state.values[key]) == platform:
                    add_entity(vin, key)

    @callback
    def _async_message_received(self, message: mqtt.ReceiveMessage) -> None:
        """Handle a single MQTT message."""

        try:
            payload = json.loads(message.payload)
        except (TypeError, json.JSONDecodeError):
            _LOGGER.debug("Ignoring non-JSON Supra Connect payload on %s", message.topic)
            return

        vin = self._extract_vin(message.topic, payload)
        if vin is None:
            _LOGGER.debug("Ignoring Supra Connect payload without VIN on %s", message.topic)
            return

        flattened = flatten_payload(payload.get("data", payload))
        flattened.pop("vin", None)
        if not flattened:
            return

        state = self.vehicles.setdefault(vin, VehicleState(vin=vin))
        now = datetime.now(timezone.utc)
        new_entities: list[tuple[str, str]] = []

        for key, value in flattened.items():
            if isinstance(value, dict | list) or value is None:
                continue
            if key not in state.values:
                platform = self.platform_for_key(key, value)
                if platform is not None:
                    new_entities.append((platform, key))
            state.values[key] = value
            state.topics[key] = message.topic

        state.values[ATTR_VIN] = vin
        state.values[ATTR_UPDATED_AT] = now.isoformat()
        state.values[ATTR_SOURCE_TOPIC] = message.topic
        state.updated_at = now

        for platform, key in new_entities:
            for add_entity in self._discovery_callbacks[platform]:
                add_entity(vin, key)

        for update_callback in self._listeners:
            update_callback()

    def _extract_vin(self, topic: str, payload: dict[str, Any]) -> str | None:
        """Extract a VIN from payload or topic."""

        payload_vin = payload.get("vin") or payload.get("VIN")
        if isinstance(payload_vin, str) and VIN_RE.fullmatch(payload_vin):
            return payload_vin.upper()

        topic_tail = topic.removeprefix(self.topic_prefix)
        topic_match = VIN_RE.search(topic_tail)
        if topic_match:
            return topic_match.group(0).upper()

        return None

    @staticmethod
    def platform_for_key(key: str, value: Any) -> str | None:
        """Choose the Home Assistant platform for a descriptor."""

        if isinstance(value, bool):
            return "binary_sensor"
        if isinstance(value, int | float | str):
            return "sensor"
        return None


def flatten_payload(payload: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    """Flatten nested telemetry dictionaries into descriptor-like keys."""

    flattened: dict[str, Any] = {}
    for key, value in payload.items():
        normalized_key = str(key)
        full_key = f"{prefix}.{normalized_key}" if prefix else normalized_key
        if isinstance(value, dict):
            if "value" in value and len(value) <= 3:
                flattened[full_key] = value["value"]
            else:
                flattened.update(flatten_payload(value, full_key))
        else:
            flattened[full_key] = value
    return flattened
