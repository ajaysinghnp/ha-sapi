"""Constants for the SAPI integration."""
from typing import Final

DOMAIN: Final = "sapi"
NAME: Final = "SAPI"
VERSION: Final = "0.0.1"

# Configuration
CONF_API_KEY = "mayasapi_key"
CONF_API_BASE_URL = "mayasapi_base_url"

# Defaults
DEFAULT_NAME = "SAPI"
DEFAULT_VERIFY_SSL = True
DEFAULT_TIMEOUT = 10  # seconds
DEFAULT_UPDATE_INTERVAL = 300  # 5 minutes

# API Endpoints/Services
API_ENDPOINT_DATE_TODAY = "/date/today"
API_ENDPOINT_DATE_TO_NEPALI = "date/to/nep"
API_ENDPOINT_DATE_TO_INT = "date/to/int"
API_ENDPOINT_GENERATE_PASSWORD = "/generate/password"
API_ENDPOINT_GENERATE_PIN = "/generate/pin"
API_ENDPOINT_UTILITIES_FORMAT_NUMBER = "utils/numbers/nep_num"
API_ENDPOINT_PAN_DETAILS = "/pan"
API_ENDPOINT_NEA_ALL = "/nea"

# Attributes
ATTR_NEPALI_DATE = "today"
ATTR_PASSWORD = "password"
ATTR_LENGTH = 20
ATTR_INCLUDE_SPECIAL = True
ATTR_PIN = "pin"
ATTR_DATE = "date"
