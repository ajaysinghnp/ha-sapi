"""
This module defines the Services handler for the integration.

Services:
- Today Date: Get todays date in various forms like nepali date, international date, with breakdown.
- Generate PIN: Generates a random PIN of specified length.
- Generate Password: Generates a random Password of specified criteria.
"""

import logging
from homeassistant.core import ServiceCall

from .const import (
    SERVICE_DATE_TODAY,
    SERVICE_GENERATE_PASSWORD,
    SERVICE_GENERATE_PIN,
    ATTR_LENGTH,
    ATTR_INCLUDE_SPECIAL,
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)

# Register services


class Services:
    def __init__(self, coordinator, hass):
        self.hass = hass
        self.coordinator = coordinator

    async def get_date_today(self, _: ServiceCall) -> None:
        """Handle Today date service call."""
        try:
            data = self.coordinator.get_cached_data(SERVICE_DATE_TODAY)
            # print(f"Storing Nepali Date in to state: {data}")
            if data:
                self.hass.states.async_set(
                    f"sensor.{SERVICE_DATE_TODAY}", data[SERVICE_DATE_TODAY])
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Failed to get Today date: %s", err)

    async def generate_password(self, call: ServiceCall) -> None:
        """Handle password generation service call."""
        length = call.data.get(ATTR_LENGTH, 12)
        include_special = call.data.get(ATTR_INCLUDE_SPECIAL, True)

        try:
            result = await self.coordinator.async_generate_password(
                # length=length,
                # include_special=include_special
            )
            _LOGGER.debug(
                "Generated password with length %s with special %s", length, include_special)
            # Store the result in hass.states
            # print(f"Storing Generated password in to state: {result}")
            self.hass.states.async_set(
                f"{DOMAIN}.{SERVICE_GENERATE_PASSWORD}", result.pop("password"))
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Failed to generate password: %s", err)

    async def generate_pin(self, call: ServiceCall) -> None:
        """Handle PIN generation service call."""
        length = call.data.get(ATTR_LENGTH, 6)

        try:
            result = await self.coordinator.async_generate_pin()
            _LOGGER.debug("Generated PIN with length %s", length)
            # print(f"Storing Generated PIN in to state: {result}")
            self.hass.states.async_set(
                f"{DOMAIN}.{SERVICE_GENERATE_PIN}", result.pop("pin"))
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Failed to generate PIN: %s", err)
