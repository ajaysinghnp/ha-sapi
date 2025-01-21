"""
This module contains unit tests for the SAPIBinarySensor class in the
custom_components.sapi.binary_sensor module.

The test_binary_sensor_state function verifies the following:
- The sensor's name is correctly set upon initialization.
- The sensor's initial state is off (is_on is False).
- The sensor's state changes to on (is_on is True) when the mock
coordinator's data indicates the sensor is active.
"""

from unittest.mock import AsyncMock
import pytest
from custom_components.sapi.binary_sensor import SAPIBinarySensor


def test_binary_sensor_state(mock_coordinator_instance):
    """Test binary sensor state."""
    sensor = SAPIBinarySensor(
        mock_coordinator_instance, "test_binary_sensor_state", "Test Sensor"
    )
    assert sensor.name == "Test Sensor"
    assert sensor.is_on is False

    # Simulate state change
    mock_coordinator_instance.data = {"is_active": True}
    sensor.async_write_ha_state()
    assert sensor.is_on is True


@pytest.mark.asyncio
async def test_binary_sensor_update(mock_coordinator_fixture):
    """Test binary sensor update."""
    sensor = SAPIBinarySensor(
        mock_coordinator_fixture, "test_binary_sensor_update", "Test Sensor"
    )
    mock_coordinator_fixture.data = {"status": "online"}

    # Trigger an update
    await sensor.async_update()
    assert sensor.is_on is True  # Replace with actual condition based on your code.


@pytest.fixture
def mock_coordinator():
    """Provide a mock coordinator for tests."""
    coordinator = AsyncMock()
    coordinator.data = {"status": "online"}
    return coordinator
