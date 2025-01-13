"""SAPI Integration for Home Assistant - Sensor Platform."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)

from .const import (
    DOMAIN,
    VERSION,
    AUTHOR,
    SERVICE_DATE_TODAY,
    SERVICE_NEA_HOME,
    SERVICE_NEA_AGRI
)

from .coordinator import SAPIDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=SERVICE_DATE_TODAY,
        name="Today",
        icon="mdi:calendar",
    ),
    SensorEntityDescription(
        key=SERVICE_NEA_HOME,
        name="NEA Home Bill",
        icon="mdi:home-battery-outline",
    ),
    SensorEntityDescription(
        key=SERVICE_NEA_AGRI,
        name="NEA Agriculture Bill",
        icon="mdi:compost",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SAPI sensors based on a config entry."""
    coordinator: SAPIDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for description in SENSOR_TYPES:
        entities.append(
            SAPISensor(
                coordinator=coordinator,
                entry_id=entry.entry_id,
                description=description,
            )
        )

    async_add_entities(entities)


class SAPISensor(CoordinatorEntity, SensorEntity):
    """Representation of a SAPI sensor."""

    def __init__(
        self,
        coordinator: SAPIDataUpdateCoordinator,
        entry_id: str,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": "SAPI Integration",
            "manufacturer": AUTHOR,
            "model": "S-API",
            "sw_version": VERSION,
        }

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        try:
            return self.coordinator.data.get(self.entity_description.key)
        except (KeyError, AttributeError):
            return None

    @property
    def extra_state_attributes(self) -> Optional[Dict[str, Any]]:
        """Return additional state attributes."""
        try:
            attributes = self.coordinator.data.get(
                f"{self.entity_description.key}_attributes", {})
            return attributes if isinstance(attributes, dict) else {}
        except (KeyError, AttributeError):
            return {}
