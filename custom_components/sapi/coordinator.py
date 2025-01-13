"""DataUpdateCoordinator for SAPI integration."""
from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import Any, Dict, Optional
import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    DEFAULT_TIMEOUT,
    DEFAULT_UPDATE_INTERVAL,
    API_ENDPOINT_DATE_TODAY,
    API_ENDPOINT_GENERATE_PASSWORD,
    API_ENDPOINT_GENERATE_PIN,
    API_ENDPOINT_NEA_ALL,
    SERVICE_DATE_TODAY,
    SERVICE_NEA_HOME,
    SERVICE_NEA_AGRI,
    SERVICE_API_HEALTH
)

_LOGGER = logging.getLogger(__name__)


class SAPIDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching SAPI data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        api_base_url: str,
        verify_ssl: bool = True,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_UPDATE_INTERVAL),
        )

        self.api_key = api_key
        # Remove trailing slash if present
        self.api_base_url = api_base_url.rstrip("/")
        self.verify_ssl = verify_ssl
        self.session = aiohttp.ClientSession()
        self._latest_data: Dict[str, Any] = {}

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from SAPI."""
        try:
            async with async_timeout.timeout(DEFAULT_TIMEOUT):
                return await self._fetch_data()
        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Timeout fetching SAPI data: {err}") from err
        except aiohttp.ClientResponseError as err:
            if err.status == 401:
                raise ConfigEntryAuthFailed("Invalid authentication") from err
            raise UpdateFailed(f"Error fetching SAPI data: {err}") from err
        except Exception as err:
            raise UpdateFailed(
                f"Unexpected error fetching SAPI data: {err}") from err

    async def _fetch_data(self) -> Dict[str, Any]:
        """Fetch data from multiple SAPI endpoints."""
        tasks = [
            self._fetch_health(),
            self._fetch_date_today(),
            self._fetch_nea_bills_summary(),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        data = {}

        # Process results and handle any individual endpoint failures
        if isinstance(results[0], Exception):
            _LOGGER.error("Failed to fetch APIs Health: %s", results[0])
            data[SERVICE_API_HEALTH] = self._latest_data.get(
                SERVICE_API_HEALTH, {})
        else:
            data[SERVICE_API_HEALTH] = results[0]["Health"] == "I am alive!"

        if isinstance(results[1], Exception):
            _LOGGER.error("Failed to fetch Today's date: %s", results[1])
            data[SERVICE_DATE_TODAY] = self._latest_data.get(
                SERVICE_DATE_TODAY, {})
            data[f"{SERVICE_DATE_TODAY}_attributes"] = self._latest_data.get(
                f"{SERVICE_DATE_TODAY}_attributes", {})
        else:
            data[SERVICE_DATE_TODAY] = results[1].pop('full_nep_date_nep')
            data[f"{SERVICE_DATE_TODAY}_attributes"] = results[1]

        if isinstance(results[2], Exception):
            _LOGGER.error("Failed to fetch NEA bills summary: %s", results[2])
            data[SERVICE_NEA_HOME] = self._latest_data.get(
                SERVICE_NEA_HOME, {})
            data[f"{SERVICE_NEA_HOME}_attributes"] = self._latest_data.get(
                f"{SERVICE_NEA_HOME}_attributes", {})
            data[SERVICE_NEA_AGRI] = self._latest_data.get(
                SERVICE_NEA_AGRI, {})
            data[f"{SERVICE_NEA_AGRI}_attributes"] = self._latest_data.get(
                f"{SERVICE_NEA_AGRI}_attributes", {})
        else:
            data[SERVICE_NEA_HOME] = results[2][0].pop("state")
            results[2][0].pop("raw_data")
            data[f"{SERVICE_NEA_HOME}_attributes"] = results[2][0]
            data[SERVICE_NEA_AGRI] = results[2][1].pop("state")
            results[2][1].pop("raw_data")
            data[f"{SERVICE_NEA_AGRI}_attributes"] = results[2][0]

        self._latest_data = data
        return data

    async def _fetch_health(self) -> Dict[str, Any]:
        """Fetch health information."""
        return await self._private_api_call("/")

    async def _fetch_date_today(self) -> Dict[str, Any]:
        """Fetch current Nepali date information."""
        return await self._private_api_call(API_ENDPOINT_DATE_TODAY)

    async def _fetch_nea_bills_summary(self) -> Dict[str, Any]:
        """Fetch bills summary information."""
        return await self._private_api_call(API_ENDPOINT_NEA_ALL)

    async def _private_api_call(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make an API call to SAPI."""
        headers = {
            "X-API-Key": f"{self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        url = f"{self.api_base_url}/{endpoint}"

        try:
            async with async_timeout.timeout(DEFAULT_TIMEOUT):
                if method == "GET":
                    async with self.session.get(
                        url,
                        headers=headers,
                        ssl=self.verify_ssl,
                    ) as resp:
                        resp.raise_for_status()
                        return await resp.json()
                elif method == "POST":
                    async with self.session.post(
                        url,
                        headers=headers,
                        json=data,
                        ssl=self.verify_ssl,
                    ) as resp:
                        resp.raise_for_status()
                        return await resp.json()

        except aiohttp.ClientResponseError as err:
            if err.status == 401:
                raise ConfigEntryAuthFailed("Invalid API key") from err
            raise UpdateFailed(f"API call failed: {err}") from err
        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"API call timed out: {err}") from err
        except Exception as err:
            raise UpdateFailed(
                f"Unexpected error during API call: {err}") from err

    # async def async_generate_password(self, length: int = 12, include_special: bool = True) -> str:
    async def async_generate_password(self) -> str:
        """Generate a password using SAPI."""
        return await self._private_api_call(API_ENDPOINT_GENERATE_PASSWORD, method="GET")

    # async def async_generate_pin(self, length: int = 6) -> str:
    async def async_generate_pin(self, _: int = 6) -> str:
        """Generate a PIN using SAPI."""
        return await self._private_api_call(API_ENDPOINT_GENERATE_PIN, method="GET")

    async def close(self) -> None:
        """Close the HTTP session."""
        if self.session:
            await self.session.close()

    def get_cached_data(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached data for a specific key."""
        return self._latest_data.get(key)

    def force_update(self) -> None:
        """Force an immediate update of the data."""
        self.async_set_updated_data(None)
