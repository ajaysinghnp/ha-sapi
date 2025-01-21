"""Global fixtures for SAPI integration tests."""

from unittest.mock import patch

import pytest
from homeassistant.core import HomeAssistant


@pytest.fixture
def hass(loop, _):
    """Return Home Assistant instance with basic configuration."""
    _hass = HomeAssistant(config_dir="/config")
    _hass.loop = loop

    async def async_setup():
        await _hass.async_start()
        await _hass.config.async_load()

    loop.run_until_complete(async_setup())

    return _hass


@pytest.fixture
def mock_setup_entry():
    """Mock setup entry."""
    with patch(
        "custom_components.sapi.async_setup_entry", return_value=True
    ) as mock_setup:
        yield mock_setup


@pytest.fixture
def mock_api():
    """Mock SAPI API responses."""
    with patch("custom_components.sapi.coordinator.SAPICoordinator") as mock:
        yield mock
