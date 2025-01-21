"""
This module contains unit tests for the custom services in the SAPI integration.

The tests are designed to ensure that the custom service calls are correctly
handled and that the appropriate methods are invoked with the expected parameters.

Tested functions:
- test_service_call: Tests the custom service call to ensure it is called with the
correct parameters.
"""

from unittest.mock import AsyncMock, patch
import pytest


@pytest.mark.asyncio
async def test_service_call(hass, _):
    """Test custom service call."""
    with patch(
        "custom_components.sapi.services.call_service", new=AsyncMock()
    ) as mock_service:
        await hass.services.async_call("sapi", "custom_service", {"param": "value"})
        mock_service.assert_called_once_with(
            "sapi", "custom_service", {"param": "value"}
        )


@pytest.mark.asyncio
async def test_service_call_failure(hass, _):
    """Test service call failure."""
    with patch(
        "custom_components.sapi.services.call_service",
        side_effect=Exception("API Error"),
    ):
        with pytest.raises(Exception, match="API Error"):
            await hass.services.async_call(
                "sapi", "custom_service", {"param": "invalid"}
            )
