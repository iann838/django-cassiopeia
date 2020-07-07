from typing import TypeVar, Type, Dict, Union, List, Mapping
import logging
import importlib
import inspect
import copy

from datapipelines import DataPipeline, DataSink, DataSource, CompositeDataTransformer, DataTransformer

from ..data import Region, Platform

T = TypeVar("T")

logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)

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

def create_pipeline(service_configs: Dict, verbose: int = 0) -> DataPipeline:
    transformers = []

    # Always use the Riot API transformers
    from ..transformers import __transformers__ as riotapi_transformer
    transformers.extend(riotapi_transformer)

    # Add sources / sinks by name from config
    services = []
    for store_name, config in service_configs.items():
        try:
            package = config.pop("package", "_cassiopeia.datastores")
        except TypeError:
            package = "_cassiopeia.datastores"
        module = importlib.import_module(name=package)
        store_cls = getattr(module, store_name)
        if store_name.lower() == "djangocache":
            for cache_config in config:
                if "expirations_map" in cache_config.keys():
                    cache_config["expirations"] = create_expiration(cache_config.pop("expirations_map"))
                services.append(store_cls(**cache_config))
        else:
            if "expirations_map" in config.keys():
                config["expirations"] = create_expiration(config.pop("expirations_map"))
            store = store_cls(**config)
            services.append(store)
            service_transformers = getattr(module, "__transformers__", [])
            transformers.extend(service_transformers)

    from ..datastores import Cache, MerakiAnalyticsCDN, LolWikia

    # Automatically insert the ghost store if it isn't there
    from ..datastores import UnloadedGhostStore
    found = False
    for datastore in services:
        if isinstance(datastore, UnloadedGhostStore):
            found = True
            break
    if not found:
        if any(isinstance(service, Cache) for service in services):
            # Find the cache and insert the ghost store directly after it
            for i, datastore in enumerate(services):
                if isinstance(datastore, Cache):
                    services.insert(i+1, UnloadedGhostStore())
                    break
        else:
            # Insert the ghost store at the beginning of the pipeline
            services.insert(0, UnloadedGhostStore())

    services.append(MerakiAnalyticsCDN())
    services.append(LolWikia())
    pipeline = DataPipeline(services, transformers)

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


def register_transformer_conversion(transformer: DataTransformer, from_type, to_type):
    # Find the method that takes a `from_type` and returns a `to_type` and register it
    methods = inspect.getmembers(transformer, predicate=inspect.ismethod)
    for name, method in methods:
        annotations = copy.copy(method.__annotations__)
        return_type = annotations.pop("return")
        annotations.pop("context", None)
        try:
            if to_type is return_type and from_type in annotations.values():
                transformer.transform.register(from_type, to_type)(method.__func__).__get__(transformer, transformer.__class__)
                break
        except TypeError:
            continue
    else:
        raise RuntimeError("Could not find method to register: {} to {} in {}.".format(from_type, to_type, transformer))


def get_default_config():
    return {
        "global": {
            "version_from_match": "patch",
            "default_region": None
        },
        "plugins": {},
        "pipeline": {
            "Cache": {},
            "DjangoCache": {},
            "DDragon": {},
            "RiotAPI": {
                "api_key": "RIOT_API_KEY"
            }
        },
        "logging": {
            "print_calls": True,
            "print_riot_api_key": False,
            "default": "WARNING",
            "core": "WARNING"
        }
    }


class Settings(object):
    def __init__(self, settings):
        _defaults = get_default_config()
        globals_ = settings.get("global", _defaults["global"])
        self.__version_from_match = globals_.get("version_from_match", _defaults["global"]["version_from_match"])  # Valid json values are: "version", "patch", and null
        self.__default_region = globals_.get("default_region", _defaults["global"]["default_region"])
        if self.__default_region is not None:
            self.__default_region = Region(self.__default_region.upper())

        self.__plugins = settings.get("plugins", _defaults["plugins"])

        self.__pipeline_args = settings.get("pipeline", _defaults["pipeline"])
        self.__pipeline = None  # type: DataPipeline

        logging_config = settings.get("logging", _defaults["logging"])
        self.__default_print_calls = logging_config.get("print_calls", _defaults["logging"]["print_calls"])
        self.__default_print_riot_api_key = logging_config.get("print_riot_api_key", _defaults["logging"]["print_riot_api_key"])
        for name in ["default", "core"]:
            logger = logging.getLogger(name)
            level = logging_config.get(name, _defaults["logging"][name])
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)

    def set_region(self, region: Union[Region, str]):
        if isinstance(region, str):
            region = Region(region.upper())
        self.__default_region = region

    @property
    def pipeline(self) -> DataPipeline:
        if self.__pipeline is None:
            self.__pipeline = create_pipeline(service_configs=self.__pipeline_args, verbose=0)
        return self.__pipeline

    @property
    def default_region(self):
        return self.__default_region

    @property
    def default_platform(self):
        return Platform[self.__default_region.name]

    @property
    def version_from_match(self):
        return self.__version_from_match

    @property
    def plugins(self):
        return self.__plugins

    def set_riot_api_key(self, key):
        from ..datastores.riotapi import RiotAPI
        for sources in self.pipeline._sources:
            for source in sources:
                if isinstance(source, RiotAPI):
                    source.set_api_key(key)

    def clear_sinks(self, type: Type[T] = None):
        types = {type}
        if type is not None:
            from ..core.common import CoreData, CassiopeiaObject
            if issubclass(type, CassiopeiaObject):
                for t in type._data_types:
                    types.add(t)
                    types.add(t._dto_type)
            elif issubclass(type, CoreData):
                types.add(type._dto_type)

        for sink in self.pipeline._sinks:
            for type in types:
                sink.clear(type)

    def expire_sinks(self, type: Type[T] = None):
        types = {type}
        if type is not None:
            from ..core.common import CoreData, CassiopeiaObject
            if issubclass(type, CassiopeiaObject):
                for t in type._data_types:
                    types.add(t)
                    types.add(t._dto_type)
            elif issubclass(type, CoreData):
                types.add(type._dto_type)

        for sink in self.pipeline._sinks:
            for type in types:
                sink.expire(type)