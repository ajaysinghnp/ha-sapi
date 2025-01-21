"""
This module provides functionality to register custom SAPI cards within the
Home Assistant frontend. It sets up a static path for the cards, enabling them
to be loaded dynamically and referenced under the specified domain.
"""

from pathlib import Path
from homeassistant.core import HomeAssistant
from homeassistant.components.http import StaticPathConfig


async def register_cards(hass: HomeAssistant, domain: str) -> None:
    """Register cards."""
    should_cache = True
    card_filepath = Path(__file__).parent / "frontend"
    card_url = f"/hacsfiles/{domain}/cards"
    await hass.http.async_register_static_paths([
        StaticPathConfig(
            card_url,
            card_filepath,
            should_cache
        )
    ])
