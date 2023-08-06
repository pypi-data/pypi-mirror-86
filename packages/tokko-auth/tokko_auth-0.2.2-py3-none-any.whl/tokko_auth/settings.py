from os import environ
from typing import Any
import logging

from django.conf import settings

from tokko_auth.exceptions import EnvVarNotInitialized
from tokko_auth.constants import COGNITO


# Local logger instance
logger = logging.getLogger(__name__)


def env_or_settings(var_name, default=None, raise_error=False) -> Any:
    """Get env var values from ENV or DJ SETTINGS"""
    try:
        _var = environ[var_name]
    except KeyError:
        _var = getattr(settings, var_name, default)
        if _var is None and raise_error:
            exception = EnvVarNotInitialized(var_name)
            logger.exception(f'{exception}')
            raise exception
    return _var


# Auth app settings
AUTH_FAIL_SAFE_ENABLE = env_or_settings("AUTH_FAIL_SAFE_ENABLE", False)
AUTH_USERINFO_ENABLE = env_or_settings("AUTH_USERINFO_ENABLE", False)
AUTH_API_NAMESPACE = env_or_settings("AUTH_API_NAMESPACE", default='')
AUTH_BEAUTIFY_ERROR_RESPONSE = env_or_settings("AUTH_BEAUTIFY_ERROR_RESPONSE", True)
AUTH_FULL_DISABLED = env_or_settings("AUTH_FULL_DISABLED", False)
AUTH_ALLOW_PRODUCTIVE_SHUTDOWN = env_or_settings(
    "AUTH_ALLOW_PRODUCTIVE_SHUTDOWN", False
)
SAMPLES_ARE_ENABLE = env_or_settings("SAMPLES_ARE_ENABLE", True)


ALGORITHMS = environ.get("TOKKO_AUTH_ALGORITHMS",
                         # Pre deprecation support
                         environ.get("ALGORITHMS",
                                     "RS256"))

API_AUDIENCE = environ.get("TOKKO_AUTH_API_AUDIENCE",
                           # Pre deprecation support
                           environ.get("API_AUDIENCE"))

AUTH_DOMAIN = environ.get("TOKKO_AUTH_PROVIDER_DOMAIN",
                          # Pre deprecation support
                          env_or_settings("AUTH0_DOMAIN", default=""))
AUTH0_DOMAIN = AUTH_DOMAIN
AUTH_STRATEGY = environ["TOKKO_AUTH_STRATEGY"] = COGNITO
