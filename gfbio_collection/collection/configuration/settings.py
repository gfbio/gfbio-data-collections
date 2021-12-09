from _csv import QUOTE_NONNUMERIC, QUOTE_NONE
from builtins import getattr

settings = {}

STATIC_GENERIC_REQUIREMENTS_LOCATION = getattr(
    settings,
    'STATIC_COMMON_REQUIREMENTS_LOCATION',
    'schemas/minimal_requirements.json'
)
