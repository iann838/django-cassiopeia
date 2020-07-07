from django.conf import settings
import copy
import sys
import _cassiopeia as cassiopeia
from logging import getLogger
LOGGER = getLogger(__name__)

def get_cass_settings():
    cass = {
        "global" : getattr(settings, "CASSIOPEIA_GLOBAL", None),
        "pipeline" : getattr(settings, "CASSIOPEIA_PIPELINE", None),
        "logging" : getattr(settings, "CASSIOPEIA_LOGGING", None),
        "plugins": getattr(settings, "CASSIOPEIA_PLUGINS", None)
    }
    for key, config in copy.deepcopy(cass).items():
        if key == "pipeline" and config is None:
            raise AttributeError("'pipeline' settings in django-cassiopeia is obligatory")
        elif config is None:
            LOGGER.warning(f"[Traceback: django-cassiopeia > settings] WARNING: '{key}' is not set, using default settings")
            del cass[key]
    for store_name, config in copy.deepcopy(cass["pipeline"]).items():
        if store_name == "DjangoCache":
            cass["pipeline"][store_name] = settings.CASSIOPEIA_DJANGO_CACHES
        elif store_name == "RiotAPI":
            cass["pipeline"][store_name]["api_key"] = settings.RIOT_API_KEY
            cass["pipeline"][store_name]["limiting_share"] = settings.CASSIOPEIA_LIMITING_SHARE
            try:
                cass["pipeline"][store_name]["request_error_handling"] = settings.CASSIOPEIA_RIOT_API_ERROR_HANDLING
            except AttributeError:
                LOGGER.warning(f"[Traceback: django-cassiopeia > settings] Warning: 'riotapi_request_error_handling' is not set, using default settings")
    return cass

cassiopeia.apply_settings(get_cass_settings())

