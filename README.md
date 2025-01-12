# SAPI Integration for Home Assistant

This custom integration allows you to use SAPI services within Home Assistant. Features include:

- Nepali date information and conversion
- Password and PIN generation
- Utility bill queries
- And more...

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on Integrations
3. Click the + button
4. Search for "SAPI"
5. Click Install

### Manual Installation

1. Copy the `custom_components/sapi` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings > Devices & Services
2. Click "+ Add Integration"
3. Search for "SAPI"
4. Enter your API key and base URL

## Services

The integration provides the following services:

### generate_password

Generate a secure password with customizable parameters.

### generate_pin

Generate a numeric PIN of specified length.

### get_nepali_date

Get the current Nepali date.

### convert_date

Convert dates between Nepali and English calendars.

### query_bill

Query utility bill information for various services.

## Support

For bugs and feature requests, please create an issue on GitHub.
