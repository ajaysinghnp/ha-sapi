# SAPI Integration for Home Assistant

This custom integration allows you to use SAPI services within Home Assistant.

## Features include

- [x] Nepali Date
- [ ] Nepali - International Date Conversion
- [x] Password generation
- [x] PIN generation
- [ ] Nepali PAN Search
- [x] Electricity bill queries
- [ ] Utility: Number Formatting and text
- [ ] State based Icons

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance.
2. Click on Integrations.
3. Click the `+` button.
4. Search for "SAPI".
5. Click Install.

### Manual Installation

1. Copy the `custom_components/sapi` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings > Devices & Services
2. Click "+ Add Integration"
3. Search for "SAPI"
4. Enter your `API_KEY`, API `base_url` and optionally a `name`
5. Choose an `area` if you are asked to choose if you want or continue.
6. Done !

## Services

The integration provides the following services:

### get_nepali_date ✅

Get the current Nepali date.

### generate_password ✅

Generate a secure password with customizable parameters.

### generate_pin ✅

Generate a numeric PIN of specified length.

### convert_date ❌

Convert dates between Nepali and English calendars.

### query_bill ✅

Query utility bill information for various services.

## Support

For bugs and feature requests, please create an issue on GitHub.

## Development Checklist

- [ ] All communication to external devices or services must be wrapped in an external Python library hosted on [pypi](https://pypi.org/).
  - [ ] The library must have source distribution packages available; it's not allowed to rely on packages that only have binary distribution packages.
  - [ ] Issue trackers must be enabled for external Python libraries that communicate with external devices or services.
  - [ ] If the library is mainly used for Home Assistant and you are a code owner of the integration, it is encouraged to use an issue template picker with links to [Home Assistant Core Issues](https://github.com/home-assistant/core/issues). For example: [zwave-js-server-python - New Issue](https://github.com/home-assistant-libs/zwave-js-server-python/issues/new/choose)
- [ ] New dependencies are added to `requirements_all.txt` (if applicable), using `python3 -m script.gen_requirements_all`
- [ ] New codeowners are added to `CODEOWNERS` (if applicable), using `python3 -m script.hassfest`
- [ ] The `.strict-typing` file is updated to include your code if it provides a fully type hinted source.
- [ ] The code is formatted using Ruff (`ruff format`).
- [ ] Documentation is developed for [home-assistant.io](https://home-assistant.io/)
  - [ ] Visit the [website documentation](https://developers.home-assistant.io/docs/documenting) for more information about contributing to [home-assistant.io](https://github.com/home-assistant/home-assistant.io).
