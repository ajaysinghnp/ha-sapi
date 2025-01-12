"""Global fixtures for SAPI integration tests."""
import pytest
from unittest.mock import patch
from homeassistant.core import HomeAssistant
from custom_components.sapi.const import DOMAIN

@pytest.fixture
def hass(loop, hass_storage):
    """Return Home Assistant instance with basic configuration."""
    hass = HomeAssistant()
    hass.loop = loop

    async def async_setup():
        await hass.async_start()
        await hass.config.async_load()
    loop.run_until_complete(async_setup())
    
    return hass

@pytest.fixture
def mock_setup_entry():
    """Mock setup entry."""
    with patch("custom_components.sapi.async_setup_entry", return_value=True) as mock_setup:
        yield mock_setup

@pytest.fixture
def mock_api():
    """Mock SAPI API responses."""
    with patch("custom_components.sapi.coordinator.SAPICoordinator") as mock:
        yield mock