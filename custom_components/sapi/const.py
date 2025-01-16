"""Constants for the SAPI integration."""
from typing import Final

DOMAIN: Final = "sapi"
NAME: Final = "SAPI"
VERSION: Final = "0.0.1"
AUTHOR: Final = "Ajay Singh"

# Configuration
CONF_API_KEY = "api_key"
CONF_API_BASE_URL = "api_base_url"
DEVICE_CLASS_BINARY = "SapiBinarySensor"

# Defaults
DEFAULT_NAME = "SAPI"
DEFAULT_VERIFY_SSL = True
DEFAULT_TIMEOUT = 10  # seconds
DEFAULT_UPDATE_INTERVAL = 1800  # 30 minutes

# API Endpoints
API_PREFIX = "/ha"
API_ENDPOINT_DATE_TODAY = "/date/today"
API_ENDPOINT_DATE_TO_NEPALI = "date/to/nep"
API_ENDPOINT_DATE_TO_INT = "date/to/int"
API_ENDPOINT_GENERATE_PASSWORD = "/generate/password"
API_ENDPOINT_GENERATE_PIN = "/generate/pin"
API_ENDPOINT_UTILITIES_FORMAT_NUMBER = "utils/numbers/nep_num"
API_ENDPOINT_PAN_DETAILS = "/pan"
API_ENDPOINT_NEA_ALL = "/nea"

# API Services
SERVICE_API_HEALTH = "health"
SERVICE_DATE_TODAY = "date_today"
SERVICE_DATE_TO_NEPALI = "date_to_nepali"
SERVICE_DATE_TO_INT = "date_to_international"
SERVICE_GENERATE_PASSWORD = "generate_password"
SERVICE_GENERATE_PIN = "generate_pin"
SERVICE_UTILITIES_FORMAT_NUMBER = "format_number"
SERVICE_PAN_DETAILS = "pan_details"
SERVICE_NEA_HOME = "nea_bill_home"
SERVICE_NEA_AGRI = "nea_bill_agri"
SERVICE_NEA_PUJA = "nea_bill_puja"
SERVICE_NEA_AMITA = "nea_bill_amita"

# Attributes
ATTR_NEPALI_DATE = "today"
ATTR_PASSWORD = "password"
ATTR_LENGTH = 20
ATTR_INCLUDE_SPECIAL = True
ATTR_PIN = "pin"
ATTR_DATE = "date"
