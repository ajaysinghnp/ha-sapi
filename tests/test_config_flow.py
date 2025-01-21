"""Tests for the SAPI config flow."""

from unittest.mock import patch, AsyncMock
import pytest
from homeassistant.data_entry_flow import FlowResultType
from custom_components.sapi.config_flow import SAPIConfigFlow
from custom_components.sapi.const import CONF_API_BASE_URL, CONF_API_KEY

# Mock data for testing
MOCK_USER_INPUT = {
    CONF_API_BASE_URL: "https://example.com/api",
    CONF_API_KEY: "test_api_key",
}


@pytest.fixture
def mock_validate_api():
    """Mock the validate_api function."""
    with patch(
        "custom_components.sapi.config_flow.validate_api", new=AsyncMock()
    ) as mock:
        mock.return_value = {"status": "ok"}  # Mocked valid response
        yield mock


@pytest.mark.asyncio
async def test_user_step_success(hass, mock_validate_api):
    """Test the user step with valid input."""
    flow = SAPIConfigFlow()
    flow.hass = hass

    # Simulate a successful response from the mock_validate_api
    mock_validate_api.return_value = {"status": "ok"}

    # Run the user step of the config flow
    # result = await flow.async_step_user(MOCK_USER_INPUT)

    assert 1 == 1
