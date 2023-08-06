import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv(dotenv_path="/Users/aa210665/Desktop/repo/cloud-storage-utility/.env")


class SupportedPlatforms(Enum):
    AZURE = "azure"
    IBM = "ibm"


def __get_from_env(key):
    value = os.getenv(key)
    if value is None:
        print(f"{key} missing from environment")
    return value


DEFAULT_PLATFORM = SupportedPlatforms.IBM

IBM_CONFIG = {
    "api_key": __get_from_env("CSUTIL_IBM_API_KEY"),
    "auth_endpoint": __get_from_env("CSUTIL_IBM_AUTH_ENDPOINT"),
    "cos_endpoint": __get_from_env("CSUTIL_IBM_COS_ENDPOINT"),
    "crn": __get_from_env("CSUTIL_IBM_CRN")
}
