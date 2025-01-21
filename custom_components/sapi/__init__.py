"""The SAPI integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_API_KEY,
    CONF_VERIFY_SSL,
    Platform,
)
from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv
from homeassistant.exceptions import ConfigEntryNotReady

from .services import Services

from .const import (
    API_PREFIX,
    DOMAIN,
    CONF_API_BASE_URL,
    SERVICE_DATE_TODAY,
    SERVICE_GENERATE_PASSWORD,
    SERVICE_GENERATE_PIN
)
from .coordinator import SAPIDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

# List of platforms to setup when the integration is loaded
PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SAPI from a config entry."""
    # Create API instance
    coordinator = SAPIDataUpdateCoordinator(
        hass,
        entry.data[CONF_API_KEY],
        f"{entry.data[CONF_API_BASE_URL]}{API_PREFIX}",
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

    # Register all services
    services = Services(coordinator, hass)
    hass.services.async_register(
        DOMAIN,
        SERVICE_DATE_TODAY,
        services.get_date_today,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GENERATE_PASSWORD,
        services.generate_password,
        supports_response=True,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GENERATE_PIN,
        services.generate_pin,
        supports_response=True,
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
                SERVICE_GENERATE_PASSWORD,
                SERVICE_GENERATE_PIN,
                SERVICE_DATE_TODAY
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
