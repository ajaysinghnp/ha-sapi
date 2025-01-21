"""Test SAPI config flow."""

from unittest.mock import patch

from homeassistant import config_entries

from custom_components.sapi.const import DOMAIN


async def test_form(hass):
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == hass.config_entries.RESULT_TYPE_FORM
    assert result["errors"] == {}

    with (
        patch(
            "custom_components.sapi.config_flow.validate_api",
            return_value=True,
        ),
        patch(
            "custom_components.sapi.async_setup_entry",
            return_value=True,
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "api_key": "test_api_key",
                "api_base_url": "http://test.url",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == hass.data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result2["title"] == "SAPI"
    assert result2["data"] == {
        "api_key": "test_api_key",
        "api_base_url": "http://test.url",
    }
