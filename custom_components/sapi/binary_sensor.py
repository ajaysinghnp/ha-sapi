"""SAPI Integration for Home Assistant - Binary Sensor Platform."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity
)

from .const import DOMAIN, AUTHOR, VERSION, SERVICE_API_HEALTH
from .coordinator import SAPIDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

BINARY_SENSOR_TYPES: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key=SERVICE_API_HEALTH,
        name="API Status",
        icon="mdi:cloud-check",
    ),
    # Add more binary sensor types as needed
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SAPI binary sensors based on a config entry."""
    coordinator: SAPIDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for description in BINARY_SENSOR_TYPES:
        entities.append(
            SAPIBinarySensor(
                coordinator=coordinator,
                entry_id=entry.entry_id,
                description=description,
            )
        )

    async_add_entities(entities)


class SAPIBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a SAPI binary sensor."""

    def __init__(
        self,
        coordinator: SAPIDataUpdateCoordinator,
        entry_id: str,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self.info = coordinator._get_info()
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": f"{self.info["app_name"]} Integration",
            "manufacturer": self.info["app_author"],
            "model": self.info["app_name"],
            "sw_version": self.info["app_version"],
        }
        return None

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        try:
            return bool(self.coordinator.data.get(self.entity_description.key))
        except (KeyError, AttributeError, TypeError):
            return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        # Consider the entity available if we have valid coordinator data
        return self.coordinator.last_update_success

    @property
    def extra_state_attributes(self) -> Optional[Dict[str, Any]]:
        """Return additional state attributes."""
        try:
            attributes = self.coordinator.data.get(
                f"{self.entity_description.key}_attributes", {})
            return attributes if isinstance(attributes, dict) else {}
        except (KeyError, AttributeError):
            return {}

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Implement any specific update handling logic here if needed
        self.async_write_ha_state()
