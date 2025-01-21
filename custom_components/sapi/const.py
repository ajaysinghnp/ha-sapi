"""Constants for the SAPI integration."""
from typing import Final
import json
from pathlib import Path

# Get the path to manifest.json
MANIFEST_PATH = Path(__file__).parent / "manifest.json"

# Read version from manifest.json
with open(MANIFEST_PATH, "r", encoding="utf-8") as manifest_file:
    manifest = json.load(manifest_file)
    DOMAIN: Final = manifest.get("domain", "sapi")
    NAME: Final = manifest.get("name", "SAPI")
    VERSION: Final = manifest.get("version", "0.0.0")

AUTHOR: Final = "Ajay Singh"

# Configuration
CONF_API_KEY: Final = "api_key"
CONF_API_BASE_URL: Final = "api_base_url"
DEVICE_CLASS_BINARY: Final = "SapiBinarySensor"

# Defaults
DEFAULT_NAME: Final = NAME
DEFAULT_VERIFY_SSL: Final = True
DEFAULT_TIMEOUT: Final = 10  # seconds
DEFAULT_UPDATE_INTERVAL: Final = 1800  # 30 minutes

# API Endpoints
API_PREFIX: Final = "/ha"
API_ENDPOINT_DATE_TODAY: Final = "/date/today"
API_ENDPOINT_DATE_TO_NEPALI: Final = "date/to/nep"
API_ENDPOINT_DATE_TO_INT: Final = "date/to/int"
API_ENDPOINT_GENERATE_PASSWORD: Final = "/generate/password"
API_ENDPOINT_GENERATE_PIN: Final = "/generate/pin"
API_ENDPOINT_UTILITIES_FORMAT_NUMBER: Final = "utils/numbers/nep_num"
API_ENDPOINT_PAN_DETAILS: Final = "/pan"
API_ENDPOINT_NEA_ALL: Final = "/nea"

# API Services
SERVICE_API_HEALTH: Final = "health"
SERVICE_DATE_TODAY: Final = "date_today"
SERVICE_DATE_TO_NEPALI: Final = "date_to_nepali"
SERVICE_DATE_TO_INT: Final = "date_to_international"
SERVICE_GENERATE_PASSWORD: Final = "generate_password"
SERVICE_GENERATE_PIN: Final = "generate_pin"
SERVICE_UTILITIES_FORMAT_NUMBER: Final = "format_number"
SERVICE_PAN_DETAILS: Final = "pan_details"
SERVICE_NEA_HOME: Final = "nea_bill_home"
SERVICE_NEA_AGRI: Final = "nea_bill_agri"
SERVICE_NEA_PUJA: Final = "nea_bill_puja"
SERVICE_NEA_AMITA: Final = "nea_bill_amita"

# Attributes
ATTR_NEPALI_DATE: Final = "today"
ATTR_PASSWORD: Final = "password"
ATTR_LENGTH: Final = 20
ATTR_INCLUDE_SPECIAL: Final = True
ATTR_PIN: Final = "pin"
ATTR_DATE: Final = "date"
