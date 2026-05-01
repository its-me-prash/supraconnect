"""Config flow for Supra Connect."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_TOPIC_PREFIX, DEFAULT_TOPIC_PREFIX, DOMAIN


class SupraConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Supra Connect config flow."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Create the integration from MQTT stream settings."""

        errors: dict[str, str] = {}

        if user_input is not None:
            topic_prefix = user_input[CONF_TOPIC_PREFIX].strip()
            if not topic_prefix:
                errors[CONF_TOPIC_PREFIX] = "empty_topic_prefix"
            else:
                await self.async_set_unique_id(f"{DOMAIN}:{topic_prefix}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data={
                        CONF_NAME: user_input[CONF_NAME],
                        CONF_TOPIC_PREFIX: topic_prefix,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default="Supra Connect"): str,
                    vol.Required(CONF_TOPIC_PREFIX, default=DEFAULT_TOPIC_PREFIX): str,
                }
            ),
            errors=errors,
            description_placeholders={"topic": f"{DEFAULT_TOPIC_PREFIX}#"},
        )
