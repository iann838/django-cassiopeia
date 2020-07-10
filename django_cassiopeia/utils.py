from typing import TypeVar, Type, Dict, Union, List, Mapping
from django.conf import settings
import copy
from logging import getLogger
LOGGER = getLogger(__name__)

expire_index = {
    "cr":"ChampionRotationData",
    "rl":"Realms",
    "v":"Versions",
    "c":"Champion",
    "c+":"Champions",
    "r":"Rune",
    "r+":"Runes",
    "i":"Item",
    "i+":"Items",
    "ss":"SummonerSpell",
    "ss+":"SummonerSpells",
    "mp":"Map",
    "mp+":"Maps",
    "pi":"ProfileIcon",
    "pi+":"ProfileIcons",
    "ls":"Locales",
    "ls+":"LanguageStrings",
    "cm":"ChampionMastery",
    "cm+":"ChampionMasteries",
    "lse":"LeagueSummonerEntries",
    "l":"League",
    "cl":"ChallengerLeague",
    "gl":"GrandmasterLeague",
    "ml":"MasterLeague",
    "m":"Match",
    "t":"Timeline",
    "s":"Summoner",
    "shs":"ShardStatus",
    "cg":"CurrentMatch",
    "fg":"FeaturedMatches",
    "rl-":"RealmDto",
    "v-":"VersionListDto",
    "c-":"ChampionDto",
    "c+-":"ChampionListDto",
    "r-":"RuneDto",
    "r+-":"RuneListDto",
    "i-":"ItemDto",
    "i+-":"ItemListDto",
    "ss-":"SummonerSpellDto",
    "ss+-":"SummonerSpellListDto",
    "mp-":"MapDto",
    "mp+-":"MapListDto",
    "pi-":"ProfileIconDetailsDto",
    "pi+-":"ProfileIconDataDto",
    "ls-":"LanguagesDto",
    "ls+-":"LanguageStringsDto",
    "cr-":"ChampionRotationDto",
    "cm-":"ChampionMasteryDto",
    "cm+-":"ChampionMasteryListDto",
    "cl-":"ChallengerLeagueListDto",
    "gl-":"GrandmasterLeagueListDto",
    "ml-":"MasterLeagueListDto",
    "m-":"MatchDto",
    "t-":"TimelineDto",
    "s-":"SummonerDto",
    "shs-":"ShardStatusDto",
    "cg-":"CurrentGameInfoDto",
    "fg-":"FeaturedGamesDto",
    "p-":"PatchListDto",
    "*-": "*-",
    "*+": "*+",
    "**": "**"
}

error_handler_map = {
    "t": {
        "strategy": "throw"
    },
    "^e": {
        "strategy": "exponential_backoff",
        1 : "initial_backoff",
        2 : "backoff_factor",
        3 : "max_attempts",
    },
    "r": {
        "strategy": "retry_from_headers",
        1 : "max_attempts",
    }
}


def create_expiration(mape) -> Mapping[type, dict]:
    expirations = {}
    last = False
    for time, types in mape.items():
        if last:
            raise AttributeError("key of type '*' is assigned but not last of object 'expirations_map'")
        for typ in types:
            if typ[0] == "*" and typ[-1] in ["*","-","+"] and len(typ) == 2:
                for mapkey, mapobj in expire_index.items():
                    key_to_add = None
                    if typ == "*-" and mapobj not in expirations.keys() and mapobj.endswith('Dto'):
                        key_to_add = mapobj
                    elif typ == "*+" and mapobj not in expirations.keys() and not mapobj.endswith('Dto'):
                        key_to_add = mapobj
                    elif typ == "**":
                        key_to_add = mapobj
                    if key_to_add is not None and key_to_add not in ["**","*-","*+"]:
                        expirations[mapobj] = time
                last = True
            elif expire_index[typ] not in expirations.keys():
                    expirations[expire_index[typ]] = time
            else:
                if typ[0] == "*":
                    raise KeyError("'"+typ+"' in object 'expirations_map'")
                raise AttributeError("Attempted duplicate key '"+typ+"' in object 'expirations_map'")
    return expirations


def create_handler(mape) -> Mapping[type, type]:
    handler = {}
    for code, values in mape.items():
        if code not in handler.keys():
            handler[code]= {}
        else:
            raise KeyError("Attempted duplicate key '"+code+"' in object 'riotapi_request_error_handling'")
        if code == "429":
            for limit_type, inner_values in values.items():
                strategy = error_handler_map[inner_values[0]]
                handler[code][limit_type] = {}
                for ind in range(len(inner_values)):
                    if ind == 0:
                        handler[code][limit_type]["strategy"] = strategy["strategy"]
                    else:
                        handler[code][limit_type][strategy[ind]] = inner_values[ind]
        else:
            for ind in range(len(values)):
                strategy = error_handler_map[values[0]]
                if ind == 0:
                    handler[code]["strategy"] = strategy["strategy"]
                else:
                    handler[code][strategy[ind]] = values[ind]
    return handler


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
                handler = settings.CASSIOPEIA_API_ERROR_HANDLING
                cass["pipeline"][store_name]["request_error_handling"] = create_handler(handler)
            except AttributeError:
                LOGGER.warning("[Traceback: django-cassiopeia > settings] Warning: 'riotapi_request_error_handling' is not set, using default settings")
                LOGGER.warning("[Traceback: django-cassiopeia > settings] Warning: 'riotapi_request_error_handling' has changed its syntax since version 1.1.0."+
                    "No longer accepts 'CASSIOPEIA_RIOT_API_ERROR_HANDLING', a shorter version is replaced on 'CASSIOPEIA_API_ERROR_HANDLING', see documentation.")
    for store_name, config in copy.deepcopy(cass["pipeline"]).items():
        if store_name.lower() == "djangocache":
            for ind in range(len(config)):
                if "expirations_map" in config[ind].keys():
                    cass["pipeline"][store_name][ind]["expirations"] = create_expiration(cass["pipeline"][store_name][ind].pop("expirations_map"))
        else:
            if "expirations_map" in config.keys():
                cass["pipeline"][store_name]["expirations"] = create_expiration(cass["pipeline"][store_name].pop("expirations_map"))
    return cass