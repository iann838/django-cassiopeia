# Setup Pipeline

Set up your pipeline settings, below is a quote from cassiopeia's [documentation](http://cassiopeia.readthedocs.org/en/latest/) explaning how cassiopeia's data pipeline works:

> The data pipeline is the series of caches, databases, and data sources (such as the Riot API) that both provide and store data. Data sources provide data, while data sinks store data; we call both of these “data stores”. Some parts of the data pipeline are only data sources (for example, the Riot API), while others are both data sources and data sinks (for example, caches and databases). The data pipeline is a list of data stores, where the order the data stores specifies how data is pulled and stored (see the next paragraph). Usually faster data stores go at the beginning of the data pipeline.

> When data is queried, a query dictionary is constructed containing the information needed to uniquely identify an object in a data source (e.g. a region and summoner.id are required when querying for Summoner objects). This query is passed up the data pipeline through the data sources, and at each data source the data pipeline asks if that source can supply the requested object. If the source can supply the object (for example, if the object is in the database, or if the Riot API can send the object/data), it is returned. If the source does not supply the object, the next data source in the pipeline is queried. If no data source can provide an object for the query, a datapipelines.NotFoundError is thrown.

> After an object is returned by a data source, the object gets passed back down the pipeline. Any data sinks along the way store the object that was returned by the data source. In this way, the cache (which should be at the front of the data pipeline) will store any object that a database or the Riot API returned.

The data pipeline used here is the same, but with the following changes:
* Lot shorter syntax for expirations settings.
* You can Log events that happens on the datastore.
* A safe check lock is in place.
* More datastores.
* Better control.

## Set your pipeline settings
File: `settings.py`

- Settings Variable: `CASSIOPEIA_PIPELINE`
- Usage: Define the structure of the pipeline.
- Accepts: Dict
    > keys: Data Stores module name.

    > values: dict of arguments or list of dict of arguments depending on the datastore specified.
- Default: No default, this settings is required otherwise an error is raised.

::: tip
A list of datastores is [later on the page](#data-stores).
:::

### Arguments
The arguments accepted varies from the datastore used.
* `"ALIAS"`: str > The name identifying the datastore if the datastore accepts multiple instances.
* `"SAFE_CHECK"`: bool > Raises an exception if some arguments are not optimal or safe to use, you can disable it by setting it to `False`, its not recommended unless you have a clear reason on doing it.
* `"LOGS_ENABLED"`: bool > Enables or disable logs for datastore events.
* `"MAX_ENTRIES"`: int > The maximum number of entries allowed in the datastore before old values are deleted, this is intended for datastore that cannot expire objects automatically on runtime.
* `"CULL_FRECUENCY"`: int > The fraction of entries that are culled when `"MAX_ENTRIES"` is reached. The actual ratio is 1 / n, where n is your value, so by setting it to 2 will cull half the entries when `"MAX_ENTRIES"` is reached.
* `"EXPIRATIONS_MAP"`: dict > Object specifying the expirations (if the datastore is a cache) for each cassiopeia object, some datastores supports `cassiopeia.core` objects, and others supports `cassiopeia.dto` objects. Most time you would combine them to give you better performance. Unlike `"expirations"` settings in cassiopeia, here you're gonna deal with a lot shorter version of it. Example:
    ```python
    from datetime import timedelta as td
    #... more settings
    "EXPIRATIONS_MAP" : {
        td(hours=3): ["c", "c+", "r", "r+", "cr", "i", "i+", "pi", "pi+"],
        td(hours=6): ["rl", "v", "ss", "ss+", "mp", "mp+", "ls", "ls+"],
        0: ["*+"]   # All remaining core objects
    }
    ```
    Below is a table with the abbrs for each object and type, they follow a similar convention but not limited to: it takes the inicials of the object's name, a `+` at the end means it contains a group (e.g. `Item` and `Items` -> `"i"` and `"i+"`), a `-` at the end means it is of type `dto`, `+-` at the end means it is a `dto` that contains a group, `**` for all the remaining objects, `*+` means all the remaining `core` objects, and `*-` for all the remaining `dto` objects. There are some exceptions with objects that has same inicials (e.g. `Realms`(`rl`) and `Rune`(`r`)).

    | Abbr | Object | type |
    | ---- | ------ | ---- |
    | `"cr"` | `ChampionRotationData` | `core` |
    | `"rl"` | `Realms` | `core` |
    | `"v"` | `Versions` | `core` |
    | `"c"` | `Champion` | `core` |
    | `"c+"` | `Champions` | `core` |
    | `"r"` | `Rune` | `core` |
    | `"r+"` | `Runes` | `core` |
    | `"i"` | `Item` | `core` |
    | `"i+"` | `Items` | `core` |
    | `"ss"` | `SummonerSpell` | `core` |
    | `"ss+"` | `SummonerSpells` | `core` |
    | `"mp"` | `Map` | `core` |
    | `"mp+"` | `Maps` | `core` |
    | `"pi"` | `ProfileIcon` | `core` |
    | `"pi+"` | `ProfileIcons` | `core` |
    | `"ls"` | `Locales` | `core` |
    | `"ls+"` | `LanguageStrings` | `core` |
    | `"cm"` | `ChampionMastery` | `core` |
    | `"cm+"` | `ChampionMasteries` | `core` |
    | `"lse"` | `LeagueSummonerEntries` | `core` |
    | `"l"` | `League` | `core` |
    | `"cl"` | `ChallengerLeague` | `core` |
    | `"gl"` | `GrandmasterLeague` | `core` |
    | `"ml"` | `MasterLeague` | `core` |
    | `"m"` | `Match` | `core` |
    | `"t"` | `Timeline` | `core` |
    | `"s"` | `Summoner` | `core` |
    | `"shs"` | `ShardStatus` | `core` |
    | `"cg"` | `CurrentMatch` | `core` |
    | `"fg"` | `FeaturedMatches` | `core` |
    | `"rl-"` | `RealmDto` | `core` |
    | `"v-"` | `VersionListDto` | `dto` |
    | `"c-"` | `ChampionDto` | `dto` |
    | `"c+-"` | `ChampionListDto` | `dto` |
    | `"r-"` | `RuneDto` | `dto` |
    | `"r+-"` | `RuneListDto` | `dto` |
    | `"i-"` | `ItemDto` | `dto` |
    | `"i+-"` | `ItemListDto` | `dto` |
    | `"ss-"` | `SummonerSpellDto` | `dto` |
    | `"ss+-"` | `SummonerSpellListDto` | `dto` |
    | `"mp-"` | `MapDto` | `dto` |
    | `"mp+-"` | `MapListDto` | `dto` |
    | `"pi-"` | `ProfileIconDetailsDto` | `dto` |
    | `"pi+-"` | `ProfileIconDataDto` | `dto` |
    | `"ls-"` | `LanguagesDto` | `dto` |
    | `"ls+-"` | `LanguageStringsDto` | `dto` |
    | `"cr-"` | `ChampionRotationDto` | `dto` |
    | `"cm-"` | `ChampionMasteryDto` | `dto` |
    | `"cm+-"` | `ChampionMasteryListDto` | `dto` |
    | `"cl-"` | `ChallengerLeagueListDto` | `dto` |
    | `"gl-"` | `GrandmasterLeagueListDto` | `dto` |
    | `"ml-"` | `MasterLeagueListDto` | `dto` |
    | `"m-"` | `MatchDto` | `dto` |
    | `"t-"` | `TimelineDto` | `dto` |
    | `"s-"` | `SummonerDto` | `dto` |
    | `"shs-"` | `ShardStatusDto` | `dto` |
    | `"cg-"` | `CurrentGameInfoDto` | `dto` |
    | `"fg-"` | `FeaturedGamesDto` | `dto` |
    | `"p-"` | `PatchListDto` | `dto` |
    | `"*-"` | Remaining of all `dto` objects |  |
    | `"*+"` | Remaining of all `core` objects |  |
    | `"**"` | Remaining of all objects |  |

## Data Stores

A list of datastores that comes with Django Cassiopeia.

### Omnistone

**_Added in 2.0:_** Due to some memory issues (specially that rows were not expiring correctly) caused by cassiopeia's `Cache` datastore during beta test, `Omnistone` is a refined version of `Cache` that fixes this issue. The issues were known before the first test release, it was ignored due to the existence of Django's Cache which was supposed to be its replacement, but the fact that Django's Cache cannot store `core` objects were slowing down significantly the performance time, and ... `Omnistone` is here lol.

- Description: This is a cache as a python object that lives on memory ONLY on server runtime, speeding up performance significantly by temporary caching `cassiopeia.core` objects, thus avoid using transformers and extra pulls. It will automatically cull the cache when a maximum entries provided in arguments is hit. This should be the first datastore in the pipeline.
- Purpose: Fixing memory issues caused by `Cache` while keeping performance.
- Supports multiple instances: No.
- Object type supported: `cassiopeia.core`
- Recommended placement on pipeline: The very first.

| Arguments | Default |
| --------- | ------- |
| `"MAX_ENTRIES"` | 6000 |
| `"CULL_FRECUENCY"` | 2 |
| `"SAFE_CHECK"` | `True` |
| `"LOGS_ENABLED"` | `False` |
| `"EXPIRATIONS_MAP"` | `{ td(hours=3): ["c", "c+", "r", "r+", "cr", "i", "i+", "pi", "pi+"], td(hours=6): ["rl", "v", "ss", "ss+", "mp", "mp+", "ls", "ls+"], 0: ["*+"] }` |

::: tip INFO
This datastore will shut down along with the Django's server, so it is not recommended to cache static data such as `Match`, `Timeline` or `Summoner`, which might actually impact a bit in performance.

The preferable way to use this datastore is to combine with datastore that doesn't shut down with server (Database, Filebased, in Memory), so the flow would be like follow: look at `core` in `Omnistone` and not found, look at `dto` in `DjangoCache` and found, now populate `Omnistone` using `core`, the next time being pulled will pull the `core` in `Omnistone` which is aprox. 5x faster.
:::

### DjangoCache

- Description: This datastore uses the Django's low-level cache API, that lets you cache `cassiopeia.dto` objects to any cache backend that works on Django.
- Purpose: Add the possibility to use the numerous flexible and production-tested caches available.
- Supports multiple instances: Yes, so its argument will take a list of dicts.
- Object type supported: `cassiopeia.dto`
- Recommended placement on pipeline: After `Omnistone`.

| Arguments | Default |
| --------- | ------- |
| `"ALIAS"` | No default, required otherwise raise error. |
| `"SAFE_CHECK"` | `True` |
| `"LOGS_ENABLED"` | `False` |
| `"EXPIRATIONS_MAP"` | `{ td(hours=6): ["rl-", "v-", "cr-", "cm-", "cm+-", "cl-", "gl-", "ml-"], td(days=7): ["mp-", "mp+-", "ls-", "ls+-", "t-", 'm-'], td(days=1): ["c-", "c+-", "r-", "r+-", "i-", "i+-", "ss-", "ss+-", "pi-", "pi+-", "p-"], td(minutes=15): ["cg-", "fg-", "shs-", "s-"], 0: ["*-"] }` |

A Django Caches settings is needed, for more information please read Django's official Cache Framework [documentation](https://docs.djangoproject.com/en/dev/topics/cache/), for example:

**Highlighted lines are cache's name, these are the `"ALIAS"` used when you define in your pipeline's settings.**
```python{6,15}
CACHES = {
    'default': {  # Do not use it for ALIAS
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    "cass-redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1,
            "COMPRESSOR": "django_redis.compressors.lz4.Lz4Compressor",
        }
    },
    'filebased': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'filebased-cache'),
        'MAX_ENTRIES': 10000,
    }
}
```
::: details Click to see details of this code.
Here we set up django_redis cache backend that uses lz4 compression before saving it to redis database, and a filebased cache that handles a maximum of 10000 files before culling.
:::
::: warning
You should ALWAYS leave `default` cache for handling caching for your app.
:::
::: tip
- Use this datastore combined with `Omnistone` for better performance.
- `MatchHistory` is bugged on the API side, thus to avoid unexpected results, this is not sinked into this datastore. Match Histories is in constant change anyways, to prevent abuse in client side you can set a limiter or throttling in DRF.
:::

### DDragon

- Description: This is a pure datasource that serves data from the League of Legends' Data Dragon.
- Supports multiple instances: No.
- Object type supported: `cassiopeia.dto`
- Recommended placement on pipeline: After any cache and before `RiotAPI`.

| Arguments | Default |
| --------- | ------- |

Does not accept any arguments.

### RiotAPI

- Description: This is a pure datasource that serves League of Legends data from the Riot API.
- Supports multiple instances: No.
- Object type supported: `cassiopeia.dto`
- Recommended placement on pipeline: The very end.

| Arguments | Default |
| --------- | ------- |

Does not accept any arguments.

_Unlike cassiopeia, you already set these arguments in `"CASSIOPEIA_RIOT_API_KEY"`, `"CASSIOPEIA_LIMITING_SHARE"` and `"CASSIOPEIA_API_ERROR_HANDLING"`._

### Cache (Deprecated)

- Description: Original Cache system used and using by cassiopeia.
- Supports multiple instances: No.
- Object type supported: `cassiopeia.core`
- Recommended placement on pipeline: The very first.

| Arguments | Default |
| --------- | ------- |
| `"EXPIRATIONS_MAP"` | The default expirations can be found in cassiopeia's [documentations](https://cassiopeia.readthedocs.io/en/latest/datapipeline.html#in-memory-cache) |

::: warning
You should not use this datastore unless a reason is given (to yourself).
It does not automatically delete objects after it is expired, which might cause memory issues in some cases.
The refined version of this datastore is [`Omnistone`](#omnistone).
:::

## Example pipeline settings
```python
CASSIOPEIA_PIPELINE = {
    "Omnistone": {
        "EXPIRATIONS_MAP" : {
            td(hours=3): ["c", "c+", "r", "r+", "cr", "i", "i+", "pi", "pi+"],
            td(hours=6): ["rl", "v", "ss", "ss+", "mp", "mp+", "ls", "ls+"],
            0: ["*+"]
        },
        "MAX_ENTRIES": 6000,
        "CULL_FRECUENCY": 2,
        "SAFE_CHECK": True,
        "LOGS_ENABLED": False,
    },
    "DjangoCache": [
        {
            "ALIAS" : "cass-redis",
            "EXPIRATIONS_MAP" : {
                td(hours=6): ["rl-", "v-", "cr-", "cm-", "cm+-", "cl-", "gl-", "ml-"],
                td(days=7): ["mp-", "mp+-", "ls-", "ls+-", "t-", 'm-'],
                td(minutes=15): ["cg-", "fg-", "shs-", "s-"],
                0: ["*-"]
            },
            "SAFE_CHECK": True,
            "LOGS_ENABLED": False,
        },
        {
            "ALIAS": "filebased",
            "EXPIRATIONS_MAP": {
                td(days=1): ["c-", "c+-", "r-", "r+-", "i-", "i+-", "ss-", "ss+-", "pi-", "pi+-", "p-"],
                0: ["*-"]
            },
            "SAFE_CHECK": True,
            "LOGS_ENABLED": False,
        }
    ],
    "DDragon": {},
    "RiotAPI": {},
}
```
::: tip
During development, you can set `"LOGS_ENABLED"` to `True` for debugging or to see if your objects are caching the way you expected, if it is not, make sure to double check the spelling (or submit an issue on github).
:::
