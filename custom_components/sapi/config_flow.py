"""Config flow for SAPI integration."""
from __future__ import annotations

import logging
from typing import Any
import voluptuous as vol
import requests

from homeassistant import config_entries
from homeassistant.const import (
    CONF_API_KEY,
    CONF_NAME,
    CONF_VERIFY_SSL,
)
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DOMAIN,
    CONF_API_BASE_URL,
    DEFAULT_NAME,
    DEFAULT_VERIFY_SSL,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
        vol.Required(CONF_API_BASE_URL): str,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Optional(CONF_VERIFY_SSL, default=DEFAULT_VERIFY_SSL): bool,
    }
)


async def validate_api(
        hass: HomeAssistant,
        # api_key: str,
        api_base_url: str,
        verify_ssl: bool
) -> bool:
    """Validate that API is working and healthy."""
    try:
        # Make the validation call in a non-blocking way
        response = await hass.async_add_executor_job(
            lambda: requests.get(
                f"{api_base_url}",
                # headers={"Authorization": f"Bearer {api_key}"},
                verify=verify_ssl,
                timeout=10,
            )
        )

        response.raise_for_status()
        return response.status_code == 200

    except requests.exceptions.SSLError as exc:
        _LOGGER.error("SSL verification failed")
        raise InvalidSSLCertificate from exc

    except requests.exceptions.ConnectionError as exc:
        _LOGGER.error("Failed to connect to SAPI")
        raise CannotConnect from exc

    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 401:
            _LOGGER.error("Invalid authentication")
            raise InvalidAuth from err
        _LOGGER.error("HTTP error occurred: %s", err)
        raise CannotConnect from err

    except requests.exceptions.Timeout as exc:
        _LOGGER.error("Timeout connecting to SAPI")
        raise CannotConnect from exc

    except Exception as err:  # pylint: disable=broad-except
        _LOGGER.error("Unknown error occurred: %s", err)
        raise CannotConnect from err


class SAPIConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SAPI."""

    VERSION = 1

    def is_matching(self, other_flow: dict[str, Any]) -> bool:
        """Check if the user input matches the existing configuration."""
        existing_entry = self._async_current_entries()
        for entry in existing_entry:
            if entry.data[CONF_API_KEY] == other_flow[CONF_API_KEY]:
                return True
        return False

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await validate_api(
                    self.hass,
                    user_input[CONF_API_BASE_URL],
                    user_input.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL),
                )

                # Check if this API key is already configured
                await self.async_set_unique_id(user_input[CONF_API_KEY])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME),
                    data={
                        CONF_API_KEY: user_input[CONF_API_KEY],
                        CONF_API_BASE_URL: user_input[CONF_API_BASE_URL],
                        CONF_VERIFY_SSL: user_input.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL),
                    },
                )

            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except InvalidSSLCertificate:
                errors["base"] = "invalid_ssl"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_reauth(self, entry_data: dict[str, Any]) -> FlowResult:
        """Handle reauthorization request."""
        _LOGGER.debug("Reauthenticating %s", entry_data[CONF_NAME])
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle reauthorization confirmation."""
        errors: dict[str, str] = {}
        entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"])

        if user_input is not None:
            try:
                await validate_api(
                    self.hass,
                    entry.data[CONF_API_BASE_URL],
                    entry.data.get(CONF_VERIFY_SSL, DEFAULT_VERIFY_SSL),
                )

                self.hass.config_entries.async_update_entry(
                    entry,
                    data={
                        **entry.data,
                        CONF_API_KEY: user_input[CONF_API_KEY],
                    },
                )
                await self.hass.config_entries.async_reload(entry.entry_id)
                return self.async_abort(reason="reauth_successful")

            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({vol.Required(CONF_API_KEY): str}),
            errors=errors,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class InvalidSSLCertificate(HomeAssistantError):
    """Error to indicate there is an invalid SSL certificate."""
