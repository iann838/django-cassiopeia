# Setup in Django environment

After installing using `pip django-cassiopeia`:

## Add app to your installed apps

File: `settings.py`
* Append `django_cassiopeia`.
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cassiopeia',
]
```

## Setup your Django's cache

File: `settings.py`
* Add the cache backends according to your needs. Below is an example of `CACHES` settings.
* `default` cache should be left for handling caching for only your app
* Add the caches that you would like to use with Cassiopeia, in this case we defined `cass-redis` cache that uses [django-redis](https://github.com/jazzband/django-redis) backend and a `filebased` cache that used Django's out of box FileBased backend.
* Any other cache backend that Django's cache framework supports can be used.
* Check out Django's cache [documentation](https://docs.djangoproject.com/en/dev/topics/cache/) for more in deep settings.
```python
# Example django cache config
CACHES = {
    # ALWAYS leave the "default" cache for handling data for your apps.
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    # Check Out "django-redis" repository/docs for lot more flexible configurations.
    "cass-redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PICKLE_VERSION": -1,
            "COMPRESSOR": "django_redis.compressors.lz4.Lz4Compressor",
        }
    },
    # Example cache using FileBased backend that stores a max of 10k values
    'filebased': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'filebased-cache'),
        'MAX_ENTRIES': 10000,
    }
}
```

## Cassiopeia specific setup

File: `settings.py`

### Define your riot api key:
* Assign your riot api key, remember to keep it secret.
* This is then mapped to `RiotAPI` argument at `Pipeline`
```python
RIOT_API_KEY = os.environ["RIOT_API_KEY"]
```

### Define your limiting share for cassiopeia:
* This feature for Django specific is still under test, defaults to 1.
* Currently rate limiting is more of "Do not black list me" scheme, needs more test to implement an actual new limiter that is compatible with Django.
```python
CASSIOPEIA_LIMITING_SHARE = 1.0
```

### Define cassiopeia globals:
* Define your `globals` settings for cassiopeia.
#### Arguments:
1. `version_from_match`: defaults to `patch`, this isn't needed now, was used when the API has different version of the same data (Currently all V4).
2. `default_region`: the region used when no region is passed on interfaces. REMINDER: `region != platform` which `NA != NA1`, the region is used.
```python
CASSIOPEIA_GLOBAL = {
    "version_from_match": "patch",
    "default_region": "NA"
}
```

### Define the logging system used for cassiopeia:
* Define how you want to log the events of cassiopeia.
#### Arguments:
1. `print_calls`: boolean, print when a call is made to Riot API
2. `print_riot_api_key`: boolean (DO NOT SET TO TRUE FOR PRODUCTION KEYS)
3. `default` & `core`: levels of the `logging` module, defaults to `WARNING`
```python
CASSIOPEIA_LOGGING = {
    "print_calls": True,
    "print_riot_api_key": False,
    "default": "WARNING",
    "core": "WARNING"
}
```
### Define the handle system for your api calls:
* Define how cassiopeia handles when a non-200 status code is generated.
* This settings might be shorten for future release (taking too much space in `settings.py`)
#### Arguments:
###### Any valid none-200 code, below arguments is for non-429s:
1. `strategy` : strategy used to handle can be of [`throw`, `exponential_backoff`, `retry_from_headers`].
2. `initial_backoff`: Unique for `exponential_backoff`, the initial time to hang a call.
3. `backoff_factor`: Unique for `exponential_backoff`, the factor to be multiplied to `initial_backoff` (exponencially) for each failed attempt.
4. `max_attempts`: Amount of time to retry, ignored by `throw`.
5. `retry_from_headers`: Retries from `"Retry-After"` value returned on response header, only for uses in 429s 
###### For 429 specific:
1. `service`: raised when an internal server limit has hit (this cannot be predicted, is a general rate limit from riot's end), applies all above arguments.
2. `method`: raised when you hit method specific rate limit, applies all above arguments.
3. `application`: raised when you hit per region rate limit, and applies all above arguments.
```python
CASSIOPEIA_RIOT_API_ERROR_HANDLING = {
    "404": {
        "strategy": "throw"
    },
    "429": {
        "service": {
            "strategy": "exponential_backoff",
            "initial_backoff": 3.0,
            "backoff_factor": 2.0,
            "max_attempts": 3
        },
        "method": {
            "strategy": "retry_from_headers",
            "max_attempts": 5
        },
        "application": {
            "strategy": "retry_from_headers",
            "max_attempts": 5
        }
    },
    "500": {
        "strategy": "exponential_backoff",
        "initial_backoff": 3.0,
        "backoff_factor": 2.0,
        "max_attempts": 3
    },
    "503": {
        "strategy": "exponential_backoff",
        "initial_backoff": 3.0,
        "backoff_factor": 2.0,
        "max_attempts": 3
    },
    "timeout": {
        "strategy": "exponential_backoff",
        "initial_backoff": 3.0,
        "backoff_factor": 2.0,
        "max_attempts": 3
    },
    "403": {
        "strategy": "throw"
    }
}
```

### IMPORTANT: Define the pipeline used for cassiopeia:
* Unlike normal settings used for cassiopeia, here for visual compatibility with Django's settings, it is splitted to different settings, the `pipeline` argument of cassiopeia is set here. The order in which you put objects matters, since that is the order that cassiopeia will look for data. `DjangoCache` is the argument for putting Django's cache into the pipeline, leave it as empty dict `{}` since it will automatically map to the `CASSIOPEIA_DJANGO_CACHES` which is set below, same happens to the `RiotAPI` argument that maps to `RIOT_API_KEY`, `CASSIOPEIA_RIOT_API_ERROR_HANDLING` and `CASSIOPEIA_LIMITING_SHARE`.
* If you want to use others Datastores for cassiopeia (such as the standard `Cache` or the plugin `SimpleKVDiskStore`), define it to the proper order on the pipeline settings, and pass any arguments such as `expirations`/`expirations-map`, `package`, etc.
* For in deep information about how the pipeline works, check out cassiopeia docs on pipelines: https://cassiopeia.readthedocs.io/en/latest/datapipeline.html
#### Arguments:
1. The name of the datastore, valid keys: `["Cache", "DjangoCache", "DDragon", "RiotAPI", "SimpleKVDiskStore", "ChampionGG", ...]`
2. And any values that the datastore needs.
```python
CASSIOPEIA_PIPELINE = {
    "DjangoCache" : {},  #look at django's cache first
    "DDragon": {},  # then to ddragon
    "RiotAPI": {},  # lastly to riot api
}
```

### Define the all the Django caches that is used for cassiopeia:
* Define the django's caches that would be used for caching cassiopeia data.
#### Arguments: 
1. `alias`: name of the cache defined in `CACHES`.
2. `logs-enabled`: enables logs of every event (PUT,GET) from and to django's caches (Recommended for testing.). 
3. `expirations`: defines the amount of time for each cassiopeia object for each cache, each pair of key-values should be in the form of `cassiopeia obj as str : datetime.timedelta obj`. This is a significant long list considering when you use multiple cache for this, `expiration-map` is a shorter version of this (see next argument). 
4. `expirations-map`: a mapping for the standard `expirations` argument, it takes a dictionary of type `datetime.timedelta obj : List[str]`, the strings inside the List is an abbr for each of the objects that cassiopeia has, normally it takes the inicials of the object's name, a `+` at the end means it contains a group (e.g. `Item` and `Items`), a `-` at the end means it is of type `dto`, `+-` at the end means it is a `dto` that contains a group, `**` for all the remaining objects, `*+` means all the remaining `core` objects, and `*-` for all the remaining `dto` objects. REMINDER: There are some exceptions with objects that has same inicials (e.g. `Realms`(`rl`) and `Rune`(`r`)). The full list of abbr is here:
```python
# List of abbrs
    "cr":"ChampionRotationData"
    "rl":"Realms"
    "v":"Versions"
    "c":"Champion"
    "c+":"Champions"
    "r":"Rune"
    "r+":"Runes"
    "i":"Item"
    "i+":"Items"
    "ss":"SummonerSpell"
    "ss+":"SummonerSpells"
    "mp":"Map"
    "mp+":"Maps"
    "pi":"ProfileIcon"
    "pi+":"ProfileIcons"
    "ls":"Locales"
    "ls+":"LanguageStrings"
    "cm":"ChampionMastery"
    "cm+":"ChampionMasteries"
    "lse":"LeagueSummonerEntries"
    "l":"League"
    "cl":"ChallengerLeague"
    "gl":"GrandmasterLeague"
    "ml":"MasterLeague"
    "m":"Match"
    "t":"Timeline"
    "s":"Summoner"
    "shs":"ShardStatus"
    "cg":"CurrentMatch"
    "fg":"FeaturedMatches"
    "rl-":"RealmDto"
    "v-":"VersionListDto"
    "c-":"ChampionDto"
    "c+-":"ChampionListDto"
    "r-":"RuneDto"
    "r+-":"RuneListDto"
    "i-":"ItemDto"
    "i+-":"ItemListDto"
    "ss-":"SummonerSpellDto"
    "ss+-":"SummonerSpellListDto"
    "mp-":"MapDto"
    "mp+-":"MapListDto"
    "pi-":"ProfileIconDetailsDto"
    "pi+-":"ProfileIconDataDto"
    "ls-":"LanguagesDto"
    "ls+-":"LanguageStringsDto"
    "cr-":"ChampionRotationDto"
    "cm-":"ChampionMasteryDto"
    "cm+-":"ChampionMasteryListDto"
    "cl-":"ChallengerLeagueListDto"
    "gl-":"GrandmasterLeagueListDto"
    "ml-":"MasterLeagueListDto"
    "m-":"MatchDto"
    "t-":"TimelineDto"
    "s-":"SummonerDto"
    "shs-":"ShardStatusDto"
    "cg-":"CurrentGameInfoDto"
    "fg-":"FeaturedGamesDto"
    "p-":"PatchListDto"
    "*-": "*-"
    "*+": "*+"
    "**": "**"
```
```python
# Example CASSIOPEIA_DJANGO_CACHES
# Here we imported `datatime.timedelta` as `td` to make it short as possible
CASSIOPEIA_DJANGO_CACHES = [
    {
        "alias" : "cass-redis",
        "expirations_map" : {
            td(hours=6): ["rl-", "v-", "cr-", "cm-", "cm+-", "cl-", "gl-", "ml-"],
            td(days=7): ["mp-", "mp+-", "ls-", "ls+-", "t-", 'm-'],
            td(minutes=15): ["cg-", "fg-", "shs-", "s-"],
            0: ["*-"]
        },
        "logs_enabled": True,
    },
    {
        "alias": "filebased",
        "expirations_imap": {
            td(days=1): ["c-", "c+-", "r-", "r+-", "i-", "i+-", "ss-", "ss+-", "pi-", "pi+-", "p-"],
            0: ["*-"]
        },
        "logs_enabled": True,
    }
]
```