"""
Tests for the SAPI config flow.

This module contains tests for the SAPI integration's configuration flow in Home Assistant.
It uses pytest and unittest.mock to mock dependencies and validate the behavior of the config flow.

Fixtures:
    mock_validate_api: A fixture that mocks the validate_api function to return a successful
    response.

Test Cases:
    test_user_step_success: Tests the user step with valid input and ensures a successful
    config entry creation.
    test_user_step_cannot_connect: Tests the user step when the API cannot connect and ensures
    the appropriate error is shown.
    test_user_step_invalid_auth: Tests the user step with invalid authentication and ensures the
    appropriate error is shown.
"""

from unittest.mock import patch, AsyncMock

import pytest
from homeassistant.data_entry_flow import FlowResultType

from custom_components.sapi.config_flow import (
    SAPIConfigFlow,
    CannotConnect,
    InvalidAuth,
)
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
async def test_user_step_success(hass, _):
    """Test the user step with valid input."""
    flow = SAPIConfigFlow()
    flow.hass = hass

    result = await flow.async_step_user(MOCK_USER_INPUT)

    assert result["type"] == hass.config_entries.FlowResultType.CREATE_ENTRY
    assert result["title"] == "SAPI"
    assert result["data"][CONF_API_BASE_URL] == MOCK_USER_INPUT[CONF_API_BASE_URL]
    assert result["data"][CONF_API_KEY] == MOCK_USER_INPUT[CONF_API_KEY]


@pytest.mark.asyncio
async def test_user_step_cannot_connect(hass):
    """Test user step when API cannot connect."""
    with patch(
        "custom_components.sapi.config_flow.validate_api",
        side_effect=CannotConnect,
    ):
        flow = SAPIConfigFlow()
        flow.hass = hass

        result = await flow.async_step_user(MOCK_USER_INPUT)

        assert result["type"] == FlowResultType.FORM
        assert result["errors"]["base"] == "cannot_connect"


@pytest.mark.asyncio
async def test_user_step_invalid_auth(hass):
    """Test user step with invalid authentication."""
    with patch(
        "custom_components.sapi.config_flow.validate_api",
        side_effect=InvalidAuth,
    ):
        flow = SAPIConfigFlow()
        flow.hass = hass

        result = await flow.async_step_user(MOCK_USER_INPUT)

        assert result["type"] == FlowResultType.FORM
        assert result["errors"]["base"] == "invalid_auth"


@pytest.mark.asyncio
async def test_reauth_flow(hass, _):
    """Test the reauth flow."""
    flow = SAPIConfigFlow()
    flow.hass = hass
    flow.context = {"entry_id": "test_id"}

    with patch(
        "custom_components.sapi.config_flow.validate_api", new=AsyncMock()
    ) as mock_validate:
        mock_validate.return_value = {"status": "ok"}
        result = await flow.async_step_reauth_confirm(MOCK_USER_INPUT)

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"
