"""
This function takes a list of integers and returns a new list containing
only the even numbers from the original list.

Parameters:
    numbers (list): A list of integers.

Returns:
    list: A list containing only the even integers from the input list.
"""

from unittest.mock import patch
import pytest


from custom_components.sapi.coordinator import SAPIDataUpdateCoordinator

# Mock data for testing
CONF_API_BASE_URL = "https://example.com/api"
CONF_API_KEY = "test_api_key"


@pytest.mark.asyncio
async def test_coordinator_update_success(hass):
    """Test successful update in coordinator."""
    coordinator = SAPIDataUpdateCoordinator(hass, CONF_API_KEY, CONF_API_BASE_URL)

    with patch(
        "custom_components.sapi.coordinator.SAPIApi.fetch_data",
        return_value={"key": "value"},
    ):
        await coordinator.async_refresh()
        assert coordinator.data == {"key": "value"}
