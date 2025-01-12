"""The SAPI integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_API_KEY,
    CONF_VERIFY_SSL,
    Platform,
)
from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv
from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
    DOMAIN,
    CONF_API_BASE_URL,
    API_ENDPOINT_GENERATE_PASSWORD,
    API_ENDPOINT_GENERATE_PIN,
    API_ENDPOINT_DATE_TODAY,
    ATTR_DATE,
    API_ENDPOINT_DATE_TO_NEPALI,
    API_ENDPOINT_DATE_TO_INT,
    API_ENDPOINT_UTILITIES_FORMAT_NUMBER,
    API_ENDPOINT_PAN_DETAILS,
    API_ENDPOINT_NEA_ALL,
    ATTR_NEPALI_DATE,
    ATTR_PASSWORD,
    ATTR_LENGTH,
    ATTR_INCLUDE_SPECIAL,
    ATTR_PIN
)
from .coordinator import SAPIDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# List of platforms to setup when the integration is loaded
PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]

# Service schemas
GENERATE_PASSWORD_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_LENGTH, default=12): vol.All(
            vol.Coerce(int), vol.Range(min=8, max=64)
        ),
        vol.Optional(ATTR_INCLUDE_SPECIAL, default=True): cv.boolean,
    }
)

GENERATE_PIN_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_LENGTH, default=4): vol.All(
            vol.Coerce(int), vol.Range(min=4, max=12)
        ),
    }
)

CONVERT_DATE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_DATE): cv.string
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SAPI from a config entry."""
    # Create API instance
    coordinator = SAPIDataUpdateCoordinator(
        hass,
        entry.data[CONF_API_KEY],
        entry.data[CONF_API_BASE_URL],
        entry.data.get(CONF_VERIFY_SSL, True),
    )

    # Fetch initial data
    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady:
        await coordinator.close()
        raise

    # Store coordinator instance
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    async def generate_password(call: ServiceCall) -> None:
        """Handle password generation service call."""
        length = call.data.get(ATTR_LENGTH, 12)
        include_special = call.data.get(ATTR_INCLUDE_SPECIAL, True)

        try:
            result = await coordinator.async_generate_password(
                length=length,
                include_special=include_special
            )
            _LOGGER.debug("Generated password with length %s", length)
            # Store the result in hass.states
            hass.states.async_set(f"{DOMAIN}.last_generated_password", result)
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Failed to generate password: %s", err)

    async def generate_pin(call: ServiceCall) -> None:
        """Handle PIN generation service call."""
        length = call.data.get(ATTR_LENGTH, 6)

        try:
            result = await coordinator.async_generate_pin(length=length)
            _LOGGER.debug("Generated PIN with length %s", length)
            hass.states.async_set(f"{DOMAIN}.last_generated_pin", result)
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Failed to generate PIN: %s", err)

    async def get_date_today(_: ServiceCall) -> None:
        """Handle Today date service call."""
        try:
            data = coordinator.get_cached_data("date_today")
            if data:
                hass.states.async_set(
                    f"{DOMAIN}.date_today", data["date"])
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Failed to get Today date: %s", err)

    # Register all services
    hass.services.async_register(
        DOMAIN,
        API_ENDPOINT_GENERATE_PASSWORD,
        generate_password,
        schema=GENERATE_PASSWORD_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        API_ENDPOINT_GENERATE_PIN,
        generate_pin,
        schema=GENERATE_PIN_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        API_ENDPOINT_DATE_TODAY,
        get_date_today,
    )

    # Entry update listener
    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        # Clean up
        coordinator = hass.data[DOMAIN][entry.entry_id]
        await coordinator.close()
        hass.data[DOMAIN].pop(entry.entry_id)

        # Remove services if this is the last entry
        if not hass.data[DOMAIN]:
            for service in [
                API_ENDPOINT_GENERATE_PASSWORD,
                API_ENDPOINT_GENERATE_PIN,
                API_ENDPOINT_DATE_TODAY
            ]:
                hass.services.async_remove(DOMAIN, service)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_migrate_entry(_: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", config_entry.version)

    if config_entry.version == 1:
        # No migration needed yet
        return True

    return False
