from typing import TypeVar, Type, Dict, Union, List, Mapping
from logging import getLogger
import importlib
import copy

from django.conf import settings
import datapipelines
import cassiopeia

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

default_logging = {
    "print_calls": True,
    "print_riot_api_key": False,
    "default": "WARNING",
    "core": "WARNING"
}

default_error = {
    "404": ["t"],
    "500": ["^e", 3, 2, 3],
    "503": ["^e", 3, 2, 3],
    "TIMEOUT": ["^e", 3, 2, 3],
    "403": ["t"],
    "429": {
        "SERVICE": ["^e", 3, 2, 3],
        "METHOD": ["r", 5],
        "APPLICATION": ["r", 5],
    },
}

def create_expiration(mape) -> Mapping[type, dict]:
    if mape is None:
        return None
    expirations = {}
    last = False
    for time, types in mape.items():
        if last:
            raise AttributeError("key of type '*' is assigned but not last of object 'EXPIRATIONS_MAP'")
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
                    raise KeyError("'"+typ+"' in object 'EXPIRATIONS_MAP'")
                raise AttributeError("Attempted duplicate key '"+typ+"' in object 'EXPIRATIONS_MAP'")
    return expirations


def create_handler(mape) -> Mapping[type, type]:
    handler = {}
    for code, values in mape.items():
        code = code.lower()
        if code not in handler.keys():
            handler[code]= {}
        else:
            raise KeyError("Attempted duplicate key '"+code+"' in object 'CASSIOPEIA_API_ERROR_HANDLER'")
        if code == "429":
            for limit_type, inner_values in values.items():
                limit_type = limit_type.lower()
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

def try_pop(obj, key):
    try:
        return obj.pop(key)
    except:
        return None


def cassiopeia_init():
    cass_global = {
        "version_from_match": getattr(settings, "CASSIOPEIA_VERSION_FROM_MATCH", "patch"),
        "default_region" : getattr(settings, "CASSIOPEIA_DEFAULT_REGION", "NA")
    }
    cass_logging = getattr(settings, "CASSIOPEIA_LOGGING", default_logging)
    cass_pipeline = {}
    settings_pipeline = getattr(settings, "CASSIOPEIA_PIPELINE", None)
    if settings_pipeline is None:
        raise AttributeError("'CASSIOPEIA_PIPELINE' settings in django-cassiopeia is obligatory")
    settings_pipeline["RiotAPI"] = {
        "api_key" : settings.CASSIOPEIA_RIOT_API_KEY,
        "limiting_share": getattr(settings,'CASSIOPEIA_LIMITING_SHARE', 1.0),
        "request_error_handling" : create_handler(getattr(settings,'CASSIOPEIA_API_ERROR_HANDLING', default_error)),
    }
    for store_name, config in settings_pipeline.items():
        if store_name.lower() == "djangocache":
            cass_pipeline[store_name] = []
            for cache in config:
                if "EXPIRATIONS_MAP" in cache.keys():
                    cache["EXPIRATIONS"] = create_expiration(try_pop(cache, "EXPIRATIONS_MAP"))
                cache = {key.lower():item for (key, item) in cache.items()}
                cass_pipeline[store_name].append(cache)
        else:
            cass_pipeline[store_name] = {}
            if "EXPIRATIONS_MAP" in config.keys():
                settings_pipeline[store_name]["EXPIRATIONS"] = create_expiration(try_pop(config, "EXPIRATIONS_MAP"))
            cass_pipeline[store_name] = {key.lower():item for (key, item) in settings_pipeline[store_name].items()}
    cassiopeia_settings = {
        "global" : cass_global,
        "pipeline" : cass_pipeline,
        "logging" : {k.lower():v for k,v in cass_logging.items()},
        "plugins": getattr(settings, "CASSIOPEIA_PLUGINS", {})
    }
    return cassiopeia_settings


def create_pipeline(service_configs: Dict, verbose: int = 0) -> datapipelines.DataPipeline:
    transformers = []

    # Always use the Riot API transformers
    from cassiopeia.transformers import __transformers__ as riotapi_transformer
    transformers.extend(riotapi_transformer)

    # Add sources / sinks by name from config
    services = []
    for store_name, config in service_configs.items():
        try:
            package = config.pop("package", "cassiopeia.datastores")
        except TypeError:
            package = "cassiopeia.datastores"
        module = importlib.import_module(name=package)
        store_cls = getattr(module, store_name)
        if store_name.lower() == "djangocache":
            for cache_config in config:
                services.append(store_cls(**cache_config))
        else:
            store = store_cls(**config)
            services.append(store)
            service_transformers = getattr(module, "__transformers__", [])
            transformers.extend(service_transformers)

    from cassiopeia.datastores import Cache, Omnistone, MerakiAnalyticsCDN, LolWikia

    # Automatically insert the ghost store if it isn't there
    from cassiopeia.datastores import UnloadedGhostStore
    found = False
    for datastore in services:
        if isinstance(datastore, UnloadedGhostStore):
            found = True
            break
    if not found:
        # Find the cache and insert the ghost store directly after it
        # OR Insert the ghost store at the beginning of the pipeline
        j = 0
        for i, datastore in enumerate(services):
            if isinstance(datastore, Cache) or isinstance(datastore, Omnistone):
                j = i+1 if i+1 > j else j
        services.insert(j, UnloadedGhostStore())

    services.append(MerakiAnalyticsCDN())
    services.append(LolWikia())
    pipeline = datapipelines.DataPipeline(services, transformers)

    if verbose > 0:
        for service in services:
            print("Service:", service)
            if verbose > 1:
                if isinstance(service, DataSource):
                    for p in service.provides:
                        print("  Provides:", p)
                if isinstance(service, DataSink):
                    for p in service.accepts:
                        print("  Accepts:", p)
        if verbose > 2:
            for transformer in transformers:
                for t in transformer.transforms.items():
                    print("Transformer:", t)
            print()

    return pipeline
