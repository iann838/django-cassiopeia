from typing import Type, Mapping, Any, Iterable, MutableMapping, TypeVar, Tuple, Callable, Generator
import datetime
import copy

from datapipelines import DataSource, DataSink, PipelineContext, Query, validate_query, NotFoundError
from backends.cache_backend import DjangoCacheBackend

from cassiopeia.data import Platform, Region, Queue, Continent
from cassiopeia.dto.common import DtoObject
from cassiopeia.dto.champion import ChampionRotationDto
from cassiopeia.dto.championmastery import ChampionMasteryDto, ChampionMasteryListDto
from cassiopeia.dto.league import MasterLeagueListDto, ChallengerLeagueListDto, GrandmasterLeagueListDto
from cassiopeia.dto.staticdata import ChampionDto, ChampionListDto, RuneDto, RuneListDto, ItemDto, ItemListDto, SummonerSpellDto, SummonerSpellListDto, MapDto, MapListDto, RealmDto, ProfileIconDataDto, ProfileIconDetailsDto, LanguagesDto, LanguageStringsDto, VersionListDto
from cassiopeia.dto.match import MatchDto, TimelineDto, MatchListDto
from cassiopeia.dto.summoner import SummonerDto
from cassiopeia.dto.status import ShardStatusDto
from cassiopeia.dto.spectator import CurrentGameInfoDto, FeaturedGamesDto
from cassiopeia.dto.patch import PatchListDto
from cassiopeia.datastores.uniquekeys import convert_region_to_platform
from cassiopeia.datastores.riotapi.common import _get_default_locale, _get_latest_version
from logging import getLogger

LOGGER = getLogger(__name__)

T = TypeVar("T")

default_expirations = {
    RealmDto: datetime.timedelta(hours=6),
    VersionListDto: datetime.timedelta(hours=6),
    ChampionDto: datetime.timedelta(days=1),
    ChampionListDto: datetime.timedelta(days=1),
    RuneDto: datetime.timedelta(days=1),
    RuneListDto: datetime.timedelta(days=1),
    ItemDto: datetime.timedelta(days=1),
    ItemListDto: datetime.timedelta(days=1),
    SummonerSpellDto: datetime.timedelta(days=1),
    SummonerSpellListDto: datetime.timedelta(days=1),
    MapDto: datetime.timedelta(days=7),
    MapListDto: datetime.timedelta(days=7),
    ProfileIconDetailsDto: datetime.timedelta(days=1),
    ProfileIconDataDto: datetime.timedelta(days=1),
    LanguagesDto: datetime.timedelta(days=7),
    LanguageStringsDto: datetime.timedelta(days=7),
    ChampionRotationDto: datetime.timedelta(hours=6),
    ChampionMasteryDto: datetime.timedelta(hours=6),
    ChampionMasteryListDto: datetime.timedelta(hours=6),
    ChallengerLeagueListDto: datetime.timedelta(hours=6),
    GrandmasterLeagueListDto: datetime.timedelta(hours=6),
    MasterLeagueListDto: datetime.timedelta(hours=6),
    MatchDto: datetime.timedelta(days=7),
    TimelineDto: datetime.timedelta(days=7),
    SummonerDto: datetime.timedelta(minutes=15),
    ShardStatusDto: datetime.timedelta(minutes=15),
    CurrentGameInfoDto: datetime.timedelta(minutes=15),
    FeaturedGamesDto: datetime.timedelta(minutes=15),
    PatchListDto: datetime.timedelta(days=1)
}


class DjangoCache(DataSource, DataSink):
    def __init__(self, expirations: Mapping[type, float] = None, alias: str = None, logs_enabled: bool = False, safe_check: bool = True) -> None:
        self._alias = alias
        self._cache = DjangoCacheBackend(alias, logs_enabled)
        self._expirations = dict(expirations) if expirations is not None else default_expirations
        #Not handling cache name check as Django will do it.
        for key, value in list(self._expirations.items()):
            if isinstance(key, str):
                if not key.endswith("Dto"):
                    raise NotImplementedError("Django's cache framework cannot cache objects of type 'cassiopeia.core'")
                new_key = globals()[key]
                self._expirations[new_key] = self._expirations.pop(key)
                key = new_key
            if value != -1 and isinstance(value, datetime.timedelta):
                self._expirations[key] = value.total_seconds()
            elif value == -1 and safe_check:
                raise RuntimeError(f"Secure check is enabled: You are trying to set {key.__name__} expiration to 'forever'")

    @DataSource.dispatch
    def get(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    @DataSink.dispatch
    def put(self, type: Type[T], item: T, context: PipelineContext = None) -> None:
        pass

    @DataSink.dispatch
    def put_many(self, type: Type[T], items: Iterable[T], context: PipelineContext = None) -> None:
        pass

    def _get(self, key: str) -> T:
        try:
            return self._cache.get(key)
        except KeyError:
            raise NotFoundError

    def _put(self, key: str, item: DtoObject) -> None:
        expire_seconds = self._expirations.get(item.__class__, default_expirations[item.__class__])
        if expire_seconds != 0:
            self._cache.put(key, item, expire_seconds)

    def _put_many(self, pairs: Mapping[str, DtoObject], clsname: DtoObject) -> None:
        expire_seconds = self._expirations.get(clsname, default_expirations[clsname])
        if expire_seconds != 0:
            self._cache.put_many(pairs, expire_seconds)

    def clear(self, type: Type[T] = None):
        self._cache.clear(type.__name__)

    # This does nothing, Django is handling expiration.
    def expire(self, type: Type[T] = None):
        self._cache.expire(type)

    ######################
    # Champion Masteries #
    ######################

    _validate_get_champion_mastery_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(str).also. \
        has("champion.id").as_(int)

    @get.register(ChampionMasteryDto)
    @validate_query(_validate_get_champion_mastery_query, convert_region_to_platform)
    def get_champion_mastery(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMasteryDto:
        champions_query = copy.deepcopy(query)
        champions_query.pop("champion.id")
        try:
            champions = self.get_champion_mastery_list(query=champions_query, context=context)
        except NotFoundError:
            raise NotFoundError

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        champion = find_matching_attribute(champions["masteries"], "championId", query["champion.id"])
        if champion is None:
            raise NotFoundError
        return ChampionMasteryDto(champion)

    _validate_get_champion_mastery_list_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(str)

    @get.register(ChampionMasteryListDto)
    @validate_query(_validate_get_champion_mastery_list_query, convert_region_to_platform)
    def get_champion_mastery_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMasteryListDto:
        self._validate_get_champion_mastery_list_query(query, context)
        platform = query["platform"].value
        summoner_id = query["summoner.id"]
        key = "{clsname}.{platform}.{summoner_id}".format(clsname=ChampionMasteryListDto.__name__,
                                                           platform=platform,
                                                           summoner_id=summoner_id)
        return ChampionMasteryListDto(self._get(key))

    @put.register(ChampionMasteryListDto)
    def put_champion_mastery_list(self, item: ChampionMasteryListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        summoner_id = item["summonerId"]
        key = "{clsname}.{platform}.{summoner_id}".format(clsname=ChampionMasteryListDto.__name__,
                                                           platform=platform,
                                                           summoner_id=summoner_id)
        self._put(key, item)

    #############
    # Champions #
    #############

    _validate_get_champion_status_list_query = Query. \
        has("platform").as_(Platform)

    @get.register(ChampionRotationDto)
    @validate_query(_validate_get_champion_status_list_query, convert_region_to_platform)
    def get_champion_status_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionRotationDto:
        platform = query["platform"].value
        key = "{clsname}.{platform}".format(clsname="ChampionRotationDto",
                                                           platform=platform)
        return ChampionRotationDto(self._get(key))

    @put.register(ChampionRotationDto)
    def put_champion_status_list(self, item: ChampionRotationDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}".format(clsname="ChampionRotationDto",
                                                           platform=platform)
        self._put(key, item)

    ###########
    # Leagues #
    ###########

    # Challenger

    _validate_get_challenger_league_query = Query. \
        has("platform").as_(Platform).also. \
        has("queue").as_(Queue)

    @get.register(ChallengerLeagueListDto)
    @validate_query(_validate_get_challenger_league_query, convert_region_to_platform)
    def get_challenger_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChallengerLeagueListDto:
        key = "{clsname}.{platform}.{queue}".format(clsname=ChallengerLeagueListDto.__name__,
                                                    platform=query["platform"].value,
                                                    queue=query["queue"].value)
        return ChallengerLeagueListDto(self._get(key))

    @put.register(ChallengerLeagueListDto)
    def put_challenger_league(self, item: ChallengerLeagueListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{queue}".format(clsname=ChallengerLeagueListDto.__name__,
                                                    platform=platform,
                                                    queue=item["queue"])
        self._put(key, item)

    # Grandmaster

    _validate_get_grandmaster_league_query = Query. \
        has("platform").as_(Platform).also. \
        has("queue").as_(Queue)

    @get.register(GrandmasterLeagueListDto)
    @validate_query(_validate_get_grandmaster_league_query, convert_region_to_platform)
    def get_grandmaster_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> GrandmasterLeagueListDto:
        key = "{clsname}.{platform}.{queue}".format(clsname=GrandmasterLeagueListDto.__name__,
                                                    platform=query["platform"].value,
                                                    queue=query["queue"].value)
        return GrandmasterLeagueListDto(self._get(key))

    @put.register(GrandmasterLeagueListDto)
    def put_grandmaster_league(self, item: GrandmasterLeagueListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{queue}".format(clsname=GrandmasterLeagueListDto.__name__,
                                                    platform=platform,
                                                    queue=item["queue"])
        self._put(key, item)

    # Master

    _validate_get_master_league_query = Query. \
        has("platform").as_(Platform).also. \
        has("queue").as_(Queue)

    @get.register(MasterLeagueListDto)
    @validate_query(_validate_get_master_league_query, convert_region_to_platform)
    def get_master_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MasterLeagueListDto:
        key = "{clsname}.{platform}.{queue}".format(clsname=MasterLeagueListDto.__name__,
                                                    platform=query["platform"].value,
                                                    queue=query["queue"].value)
        return MasterLeagueListDto(self._get(key))

    @put.register(MasterLeagueListDto)
    def put_master_league(self, item: MasterLeagueListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{queue}".format(clsname=MasterLeagueListDto.__name__,
                                                    platform=platform,
                                                    queue=item["queue"])
        self._put(key, item)

    #########
    # Match #
    #########

    # Match

    _validate_get_match_query = Query. \
        has("id").as_(str).also. \
        has("continent").as_(Continent)

    @get.register(MatchDto)
    @validate_query(_validate_get_match_query, convert_region_to_platform)
    def get_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchDto:
        key = "{clsname}.{platform}.{id}".format(clsname=MatchDto.__name__,
                                                 platform=query["continent"].value,
                                                 id=query["id"])
        return MatchDto(self._get(key))

    @put.register(MatchDto)
    def put_match(self, item: MatchDto, context: PipelineContext = None) -> None:
        platform = Continent(item["continent"]).value
        key = "{clsname}.{platform}.{id}".format(clsname=MatchDto.__name__,
                                                 platform=platform,
                                                 id=item["matchId"])
        self._put(key, item)

    # Match list

    # This is cool and useful functionality, but it really only works if we can pull the entire match
    # history in one go. For now, we just won't save the match history to disk at all.
    """
    _validate_get_match_list_query = Query. \
        has("account.id").as_(int).also. \
        has("platform").as_(Platform).also. \
        can_have("beginTime").as_(int).also. \
        can_have("endTime").as_(int).also. \
        can_have("beginIndex").as_(int).also. \
        can_have("endIndex").as_(int).also. \
        can_have("seasons").as_(Iterable).also. \
        can_have("champion.ids").as_(Iterable).also. \
        can_have("queues").as_(Iterable).also. \
        can_have("forceRefresh").with_default(False)
    @get.register(MatchListDto)
    def get_match_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchListDto:
        MatchDiskService._validate_get_match_list_query(query, context)
        platform = query["platform"].value
        queues = "|".join(sorted({queue.value for queue in query.get("queues", {})}))
        seasons = "|".join(sorted({season.value for season in query.get("seasons", {})}))
        champions = "|".join(sorted({champion.value for champion in query.get("champion.ids", {})}))
        key = "{clsname}.{platform}.{account_id}.{queues}.{seasons}.{champions}".format(clsname=MatchListDto.__name__,
                                                                                        platform=platform,
                                                                                        account_id=query["account.id"],
                                                                                        queues=queues,
                                                                                        seasons=seasons,
                                                                                        champions=champions)
        data = self._get(key)
        # The above line will throw a NotFoundError if the matchlist for this summoner doesn't exist at all.
        # However, if it does exist, let's try to be smart about pulling the remaining data.
        most_recent = data["matches"][0]["timestamp"]
        # Choose 30 minutes to refresh match history
        refresh_from_expiration = datetime.datetime.fromtimestamp(most_recent/1000) < datetime.datetime.now() - datetime.timedelta(minutes=30)
        if query["forceRefresh"] or refresh_from_expiration:
            new_query = copy.deepcopy(query)
            new_query.pop("beginTime", None)
            new_query.pop("endTime", None)
            new_query.pop("beginIndex", None)
            new_query.pop("endIndex", None)
            new_query["beginTime"] = most_recent + 1  # Add 1 ms so we don't get the last game we have.
            new_data = context[context.Keys.PIPELINE].get(MatchListDto, query=new_query, context=context)
            data["matches"].extend(new_data["matches"])
        return MatchListDto(self._get(key))
    @put.register(MatchListDto)
    def put_match_list(self, item: MatchListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        queues = "|".join(sorted({queue.value for queue in item["queue"]}))
        seasons = "|".join(sorted({season.value for season in item["season"]}))
        champions = "|".join(sorted({champion.value for champion in item["champion"]}))
        key = "{clsname}.{platform}.{account_id}.{queues}.{seasons}.{champions}".format(clsname=MatchListDto.__name__,
                                                                                        platform=platform,
                                                                                        account_id=item["accountId"],
                                                                                        queues=queues,
                                                                                        seasons=seasons,
                                                                                        champions=champions)
        self._put(key, item)
    """

    # Timeline

    _validate_get_timeline_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(TimelineDto)
    @validate_query(_validate_get_timeline_query, convert_region_to_platform)
    def get_timeline(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> TimelineDto:
        key = "{clsname}.{platform}.{id}".format(clsname=TimelineDto.__name__,
                                                 platform=query["platform"].value,
                                                 id=query["id"])
        return TimelineDto(self._get(key))

    @put.register(TimelineDto)
    def put_timeline(self, item: TimelineDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{id}".format(clsname=TimelineDto.__name__,
                                                 platform=platform,
                                                 id=item["matchId"])
        self._put(key, item)

    #########
    # Patch #
    #########

    @get.register(PatchListDto)
    def get_patches(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> PatchListDto:
        key = "{clsname}".format(clsname=PatchListDto.__name__)
        return PatchListDto(self._get(key))

    @put.register(PatchListDto)
    def put_patches(self, item: PatchListDto, context: PipelineContext = None) -> None:
        key = "{clsname}".format(clsname=PatchListDto.__name__)
        self._put(key, item)

    ##################
    # Featured Games #
    ##################

    _validate_get_featured_games_query = Query. \
        has("platform").as_(Platform)

    @get.register(FeaturedGamesDto)
    @validate_query(_validate_get_featured_games_query, convert_region_to_platform)
    def get_featured_games(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> FeaturedGamesDto:
        key = "{clsname}.{platform}".format(clsname=FeaturedGamesDto.__name__, platform=query["platform"].value)
        return FeaturedGamesDto(self._get(key))

    @put.register(FeaturedGamesDto)
    def put_featured_games(self, item: FeaturedGamesDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}".format(clsname=FeaturedGamesDto.__name__, platform=platform)
        self._put(key, item)

    ################
    # Current Game #
    ################

    _validate_get_current_game_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(str)

    @get.register(CurrentGameInfoDto)
    @validate_query(_validate_get_current_game_query, convert_region_to_platform)
    def get_current_game(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> CurrentGameInfoDto:
        key = "{clsname}.{platform}.{id}".format(clsname=CurrentGameInfoDto.__name__,
                                                 platform=query["platform"].value,
                                                 id=query["summoner.id"])
        return CurrentGameInfoDto(self._get(key))

    @put.register(CurrentGameInfoDto)
    def put_current_game(self, item: CurrentGameInfoDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{id}".format(clsname=CurrentGameInfoDto.__name__,
                                                 platform=platform,
                                                 id=item["summonerId"])
        self._put(key, item)

    ############
    # Versions #
    ############

    _validate_get_versions_query = Query. \
        has("platform").as_(Platform)

    @get.register(VersionListDto)
    @validate_query(_validate_get_versions_query, convert_region_to_platform)
    def get_versions(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> VersionListDto:
        key = "{clsname}.{platform}".format(clsname=VersionListDto.__name__, platform=query["platform"].value)
        return VersionListDto(self._get(key))

    @put.register(VersionListDto)
    def put_versions(self, item: VersionListDto, context: PipelineContext = None) -> None:
        key = "{clsname}.{platform}".format(clsname=VersionListDto.__name__, platform=Region(item["region"]).platform.value)
        self._put(key, item)

    ##########
    # Realms #
    ##########

    _validate_get_realms_query = Query. \
        has("platform").as_(Platform)

    @get.register(RealmDto)
    @validate_query(_validate_get_realms_query, convert_region_to_platform)
    def get_realms(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RealmDto:
        key = "{clsname}.{platform}".format(clsname=RealmDto.__name__, platform=query["platform"].value)
        return RealmDto(self._get(key))

    @put.register(RealmDto)
    def put_realms(self, item: RealmDto, context: PipelineContext = None) -> None:
        key = "{clsname}.{platform}".format(clsname=RealmDto.__name__, platform=Region(item["region"]).platform.value)
        self._put(key, item)

    #############
    # Champions #
    #############

    _validate_get_champion_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(ChampionDto)
    @validate_query(_validate_get_champion_query, convert_region_to_platform)
    def get_champion(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionDto:
        champions_query = copy.deepcopy(query)
        if "id" in champions_query:
            champions_query.pop("id")
        if "name" in champions_query:
            champions_query.pop("name")
        champions = context[context.Keys.PIPELINE].get(ChampionListDto, query=champions_query)

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        if "id" in query:
            champion = find_matching_attribute(champions["data"].values(), "id", query["id"])
        elif "name" in query:
            champion = find_matching_attribute(champions["data"].values(), "name", query["name"])
        else:
            raise ValueError("Impossible!")
        if champion is None:
            raise NotFoundError
        champion["region"] = query["platform"].region.value
        champion["version"] = query["version"]
        champion["locale"] = query["locale"]
        champion["includedData"] = query["includedData"]
        return ChampionDto(champion)

    _validate_get_champion_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(ChampionListDto)
    @validate_query(_validate_get_champion_list_query, convert_region_to_platform)
    def get_champion_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionListDto:
        platform = query["platform"].value
        version = query["version"]
        locale = query["locale"]
        included_data = "|".join(sorted(query["includedData"]))
        key = "{clsname}.{platform}.{version}.{locale}.{included_data}".format(clsname=ChampionListDto.__name__,
                                                                                            platform=platform,
                                                                                            version=version,
                                                                                            locale=locale,
                                                                                            included_data=included_data)
        data = self._get(key)
        data["data"] = {key: ChampionDto(champion) for key, champion in data["data"].items()}
        return ChampionListDto(data)

    @put.register(ChampionListDto)
    def put_champion_list(self, item: ChampionListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        included_data = "|".join(sorted(item["includedData"]))
        key = "{clsname}.{platform}.{version}.{locale}.{included_data}".format(clsname=ChampionListDto.__name__,
                                                                                            platform=platform,
                                                                                            version=item["version"],
                                                                                            locale=item["locale"],
                                                                                            included_data=included_data)
        self._put(key, item)

    #########
    # Items #
    #########

    _validate_get_item_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(ItemDto)
    @validate_query(_validate_get_item_query, convert_region_to_platform)
    def get_item(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ItemDto:
        items_query = copy.deepcopy(query)
        if "id" in items_query:
            items_query.pop("id")
        if "name" in items_query:
            items_query.pop("name")
        items = context[context.Keys.PIPELINE].get(ItemListDto, query=items_query)

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        if "id" in query:
            item = find_matching_attribute(items["data"].values(), "id", query["id"])
        elif "name" in query:
            item = find_matching_attribute(items["data"].values(), "name", query["name"])
        else:
            raise ValueError("Impossible!")
        if item is None:
            raise NotFoundError
        item["region"] = query["platform"].region.value
        item["version"] = query["version"]
        item["locale"] = query["locale"]
        item["includedData"] = query["includedData"]
        return ItemDto(item)

    _validate_get_item_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(ItemListDto)
    @validate_query(_validate_get_item_list_query, convert_region_to_platform)
    def get_item_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ItemListDto:
        platform = query["platform"].value
        version = query["version"]
        locale = query["locale"]
        included_data = "|".join(sorted(query["includedData"]))
        key = "{clsname}.{platform}.{version}.{locale}.{included_data}".format(clsname=ItemListDto.__name__,
                                                                               platform=platform,
                                                                               version=version,
                                                                               locale=locale,
                                                                               included_data=included_data)
        data = self._get(key)
        for key, item in data["data"].items():
            item = ItemDto(item)
            data["data"][key] = item
        return ItemListDto(data)

    @put.register(ItemListDto)
    def put_item_list(self, item: ItemListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        included_data = "|".join(sorted(item["includedData"]))
        key = "{clsname}.{platform}.{version}.{locale}.{included_data}".format(clsname=ItemListDto.__name__,
                                                                               platform=platform,
                                                                               version=item["version"],
                                                                               locale=item["locale"],
                                                                               included_data=included_data)
        self._put(key, item)

    ##################
    # SummonerSpells #
    ##################

    _validate_get_summoner_spell_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(SummonerSpellDto)
    @validate_query(_validate_get_summoner_spell_query, convert_region_to_platform)
    def get_summoner_spell(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerSpellDto:
        summoner_spells_query = copy.deepcopy(query)
        if "id" in summoner_spells_query:
            summoner_spells_query.pop("id")
        if "name" in summoner_spells_query:
            summoner_spells_query.pop("name")
        summoner_spells = context[context.Keys.PIPELINE].get(SummonerSpellListDto, query=summoner_spells_query)

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        if "id" in query:
            summoner_spell = find_matching_attribute(summoner_spells["data"].values(), "id", query["id"])
        elif "name" in query:
            summoner_spell = find_matching_attribute(summoner_spells["data"].values(), "name", query["name"])
        else:
            raise ValueError("Impossible!")
        if summoner_spell is None:
            raise NotFoundError
        summoner_spell["region"] = query["platform"].region.value
        summoner_spell["version"] = query["version"]
        summoner_spell["locale"] = query["locale"]
        summoner_spell["includedData"] = query["includedData"]
        return SummonerSpellDto(summoner_spell)

    _validate_get_summoner_spell_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(SummonerSpellListDto)
    @validate_query(_validate_get_summoner_spell_list_query, convert_region_to_platform)
    def get_summoner_spell_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerSpellListDto:
        platform = query["platform"].value
        version = query["version"]
        locale = query["locale"]
        included_data = "|".join(sorted(query["includedData"]))
        key = "{clsname}.{platform}.{version}.{locale}.{included_data}".format(clsname=SummonerSpellListDto.__name__,
                                                                               platform=platform,
                                                                               version=version,
                                                                               locale=locale,
                                                                               included_data=included_data)
        return SummonerSpellListDto(self._get(key))

    @put.register(SummonerSpellListDto)
    def put_summoner_spell_list(self, item: SummonerSpellListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        included_data = "|".join(sorted(item["includedData"]))
        key = "{clsname}.{platform}.{version}.{locale}.{included_data}".format(clsname=SummonerSpellListDto.__name__,
                                                                               platform=platform,
                                                                               version=item["version"],
                                                                               locale=item["locale"],
                                                                               included_data=included_data)
        self._put(key, item)

    ########
    # Maps #
    ########

    _validate_get_map_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    @get.register(MapDto)
    @validate_query(_validate_get_map_query, convert_region_to_platform)
    def get_map(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MapDto:
        maps_query = copy.deepcopy(query)
        if "id" in maps_query:
            maps_query.pop("id")
        if "name" in maps_query:
            maps_query.pop("name")
        maps = context[context.Keys.PIPELINE].get(MapListDto, query=maps_query)

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        if "id" in query:
            map = find_matching_attribute(maps["data"].values(), "mapId", str(query["id"]))
        elif "name" in query:
            map = find_matching_attribute(maps["data"].values(), "mapName", query["name"])
        else:
            raise ValueError("Impossible!")
        if map is None:
            raise NotFoundError
        map["region"] = query["platform"].region.value
        map["version"] = query["version"]
        map["locale"] = query["locale"]
        return MapDto(map)

    _validate_get_map_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    @get.register(MapListDto)
    @validate_query(_validate_get_map_list_query, convert_region_to_platform)
    def get_map_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MapListDto:
        platform = query["platform"].value
        version = query["version"]
        locale = query["locale"]
        key = "{clsname}.{platform}.{version}.{locale}".format(clsname=MapListDto.__name__,
                                                               platform=platform,
                                                               version=version,
                                                               locale=locale)
        return MapListDto(self._get(key))

    @put.register(MapListDto)
    def put_map_list(self, item: MapListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{version}.{locale}".format(clsname=MapListDto.__name__,
                                                               platform=platform,
                                                               version=item["version"],
                                                               locale=item["locale"])
        self._put(key, item)

    #################
    # Profile Icons #
    #################

    _validate_get_profile_icons_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    @get.register(ProfileIconDataDto)
    @validate_query(_validate_get_profile_icons_query, convert_region_to_platform)
    def get_profile_icons(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ProfileIconDataDto:
        platform = query["platform"].value
        version = query["version"]
        locale = query["locale"]
        key = "{clsname}.{platform}.{version}.{locale}".format(clsname=ProfileIconDataDto.__name__,
                                                               platform=platform,
                                                               version=version,
                                                               locale=locale)
        return ProfileIconDataDto(self._get(key))

    @put.register(ProfileIconDataDto)
    def put_profile_icons(self, item: ProfileIconDataDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{version}.{locale}".format(clsname=ProfileIconDataDto.__name__,
                                                               platform=platform,
                                                               version=item["version"],
                                                               locale=item["locale"])
        self._put(key, item)

    ############
    # Language #
    ############

    _validate_get_languages_query = Query. \
        has("platform").as_(Platform)

    @get.register(LanguagesDto)
    @validate_query(_validate_get_languages_query, convert_region_to_platform)
    def get_language(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguagesDto:
        platform = query["platform"].value
        key = "{clsname}.{platform}".format(clsname=LanguagesDto.__name__, platform=platform)
        return LanguagesDto(self._get(key))

    _validate_get_many_languages_query = Query. \
        has("platforms").as_(Iterable)

    @put.register(LanguagesDto)
    def put_language(self, item: LanguagesDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}".format(clsname=LanguagesDto.__name__, platform=platform)
        self._put(key, item)

    ####################
    # Language Strings #
    ####################

    _validate_get_language_strings_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    @get.register(LanguageStringsDto)
    @validate_query(_validate_get_language_strings_query, convert_region_to_platform)
    def get_language_strings(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguageStringsDto:
        platform = query["platform"].value
        version = query["version"]
        locale = query["locale"]
        key = "{clsname}.{platform}.{version}.{locale}".format(clsname=LanguageStringsDto.__name__,
                                                               platform=platform,
                                                               version=version,
                                                               locale=locale)
        return LanguageStringsDto(self._get(key))

    _validate_get_many_language_strings_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str)

    @put.register(LanguageStringsDto)
    def put_language_strings(self, item: LanguageStringsDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{version}.{locale}".format(clsname=LanguageStringsDto.__name__,
                                                               platform=platform,
                                                               version=item["version"],
                                                               locale=item["locale"])
        self._put(key, item)

    #########
    # Runes #
    #########

    _validate_get_rune_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(RuneDto)
    @validate_query(_validate_get_rune_query, convert_region_to_platform)
    def get_rune(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RuneDto:
        runes_query = copy.deepcopy(query)
        if "id" in runes_query:
            runes_query.pop("id")
        if "name" in runes_query:
            runes_query.pop("name")
        runes = context[context.Keys.PIPELINE].get(RuneListDto, query=runes_query)

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        if "id" in query:
            rune = find_matching_attribute(runes["data"], "runeId", str(query["id"]))
        elif "name" in query:
            rune = find_matching_attribute(runes["data"], "runeName", query["name"])
        else:
            raise ValueError("Impossible!")
        if rune is None:
            raise NotFoundError
        rune["region"] = query["platform"].region.value
        rune["version"] = query["version"]
        rune["locale"] = query["locale"]
        return RuneDto(rune)

    _validate_get_rune_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    @get.register(RuneListDto)
    @validate_query(_validate_get_rune_list_query, convert_region_to_platform)
    def get_rune_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RuneListDto:
        platform = query["platform"].value
        version = query["version"]
        locale = query["locale"]
        key = "{clsname}.{platform}.{version}.{locale}".format(clsname=RuneListDto.__name__,
                                                               platform=platform,
                                                               version=version,
                                                               locale=locale)
        return RuneListDto(self._get(key))

    @put.register(RuneListDto)
    def put_rune_list(self, item: RuneListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{version}.{locale}".format(clsname=RuneListDto.__name__,
                                                               platform=platform,
                                                               version=item["version"],
                                                               locale=item["locale"])
        self._put(key, item)

    ##########
    # Status #
    ##########

    _validate_get_status_query = Query. \
        has("platform").as_(Platform)

    @get.register(ShardStatusDto)
    @validate_query(_validate_get_status_query, convert_region_to_platform)
    def get_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ShardStatusDto:
        key = "{clsname}.{platform}".format(clsname=ShardStatusDto.__name__, platform=query["platform"].value)
        return ShardStatusDto(self._get(key))

    @put.register(ShardStatusDto)
    def put_status(self, item: ShardStatusDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}".format(clsname=ShardStatusDto.__name__, platform=platform)
        self._put(key, item)

    ############
    # Summoner #
    ############

    _validate_get_summoner_query = Query. \
        has("id").as_(str). \
        or_("accountId").as_(str). \
        or_("puuid").as_(str). \
        or_("name").as_(str).also. \
        has("platform").as_(Platform)

    @get.register(SummonerDto)
    @validate_query(_validate_get_summoner_query, convert_region_to_platform)
    def get_summoner(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerDto:
        platform_str  = query["platform"].value
        key_attr = None
        for id_type in ["name", "accountId", "id", "puuid"]:
            key_attr = query.get(id_type, None)
            if key_attr is not None:
                break
        key = "{clsname}.{platform}.{value}".format(clsname=SummonerDto.__name__,
                                                    platform=platform_str,
                                                    value=key_attr)
        return SummonerDto(self._get(key))

    @put.register(SummonerDto)
    def put_summoner(self, item: SummonerDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        pairs = {}
        for id_type in ["name", "accountId", "id", "puuid"]:
            key = "{clsname}.{platform}.{value}".format(clsname=SummonerDto.__name__,
                                                        platform=platform,
                                                        value=item[id_type])
            pairs[key] = item
        self._put_many(pairs, SummonerDto)
